from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PerfilUsuario, Permissao, GrupoPermissao, UsuarioPermissao, LogAcesso

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()
    nome_completo = serializers.CharField(source='usuario.get_full_name', read_only=True)
    email = serializers.CharField(source='usuario.email', read_only=True)
    username = serializers.CharField(source='usuario.username', read_only=True)
    endereco_completo = serializers.SerializerMethodField()
    
    def get_endereco_completo(self, obj):
        try:
            return obj.get_endereco_completo() if hasattr(obj, 'get_endereco_completo') else ''
        except Exception:
            return ''
    
    class Meta:
        model = PerfilUsuario
        fields = '__all__'
        read_only_fields = ['criado_em', 'atualizado_em', 'criado_por']
    
    def validate(self, data):
        # Obter dados do usuário do request
        request = self.context.get('request')
        if request and hasattr(request, 'data'):
            request_data = request.data
        else:
            request_data = {}
        user_data = request_data.get('usuario', {})
        
        # Se não há dados de usuário, permitir (atualização parcial)
        if not user_data:
            return data
        
        # Se é uma criação (não tem instance), validar campos obrigatórios
        if not self.instance:
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if not user_data.get(field):
                    raise serializers.ValidationError(f"Campo {field} é obrigatório")
            
            # Validar se username já existe
            if User.objects.filter(username=user_data.get('username')).exists():
                raise serializers.ValidationError("Nome de usuário já existe")
            
            # Validar se email já existe
            if User.objects.filter(email=user_data.get('email')).exists():
                raise serializers.ValidationError("Email já existe")
        
        # Se é uma atualização, validar apenas se os campos foram fornecidos
        else:
            # Se username foi fornecido, verificar se já existe (exceto para o próprio usuário)
            if 'username' in user_data and user_data['username'] != self.instance.usuario.username:
                if User.objects.filter(username=user_data['username']).exists():
                    raise serializers.ValidationError("Nome de usuário já existe")
            
            # Se email foi fornecido, verificar se já existe (exceto para o próprio usuário)
            if 'email' in user_data and user_data['email'] != self.instance.usuario.email:
                if User.objects.filter(email=user_data['email']).exists():
                    raise serializers.ValidationError("Email já existe")
        
        return data
    
    def get_usuario(self, obj):
        return {
            'id': obj.usuario.id,
            'username': obj.usuario.username,
            'email': obj.usuario.email,
            'first_name': obj.usuario.first_name,
            'last_name': obj.usuario.last_name
        }
    
    def create(self, validated_data):
        try:
            # Criar usuário Django primeiro
            request = self.context.get('request')
            if request and hasattr(request, 'data'):
                request_data = request.data
            else:
                request_data = {}
            user_data = request_data.get('usuario', {})
            
            user = User.objects.create_user(
                username=user_data.get('username'),
                email=user_data.get('email'),
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
                password=user_data.get('password')
            )
            
            # Criar perfil com status correto
            validated_data['usuario'] = user
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                validated_data['criado_por'] = request.user
            else:
                validated_data['criado_por'] = None
            
            # Garantir que o status seja 'ativo' por padrão se não foi especificado
            if 'status' not in validated_data or not validated_data['status']:
                validated_data['status'] = 'ativo'
                
            # Garantir que o nível de acesso seja definido
            if 'nivel_acesso' not in validated_data or not validated_data['nivel_acesso']:
                validated_data['nivel_acesso'] = 'usuario'
                
            # Criar o perfil
            perfil = super().create(validated_data)
            
            # Verificar se foi criado corretamente
            if not perfil:
                raise Exception("Erro ao criar perfil de usuário")
                
            return perfil
            
        except Exception as e:
            # Se houver erro, tentar limpar o usuário criado
            if 'user' in locals():
                try:
                    user.delete()
                except:
                    pass
            raise e
    
    def update(self, instance, validated_data):
        # Atualizar usuário Django se necessário
        request = self.context.get('request')
        if request and hasattr(request, 'data'):
            request_data = request.data
        else:
            request_data = {}
        user_data = request_data.get('usuario', {})
        
        if user_data:
            user = instance.usuario
            if 'email' in user_data:
                user.email = user_data['email']
            if 'first_name' in user_data:
                user.first_name = user_data['first_name']
            if 'last_name' in user_data:
                user.last_name = user_data['last_name']
            if 'password' in user_data:
                user.set_password(user_data['password'])
            user.save()
        
        return super().update(instance, validated_data)

class PerfilUsuarioListSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()
    nome_completo = serializers.CharField(source='usuario.get_full_name', read_only=True)
    email = serializers.CharField(source='usuario.email', read_only=True)
    username = serializers.CharField(source='usuario.username', read_only=True)
    ultimo_acesso_formatado = serializers.SerializerMethodField()
    
    class Meta:
        model = PerfilUsuario
        fields = [
            'id', 'usuario', 'nome_completo', 'username', 'email', 'nivel_acesso',
            'status', 'cargo', 'departamento', 'ultimo_acesso_formatado', 'criado_em'
        ]
    
    def get_usuario(self, obj):
        return {
            'id': obj.usuario.id,
            'username': obj.usuario.username,
            'email': obj.usuario.email,
            'first_name': obj.usuario.first_name,
            'last_name': obj.usuario.last_name
        }
    
    def get_ultimo_acesso_formatado(self, obj):
        if obj.ultimo_acesso:
            return obj.ultimo_acesso.strftime('%d/%m/%Y %H:%M')
        return 'Nunca acessou'

class PermissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissao
        fields = '__all__'

class GrupoPermissaoSerializer(serializers.ModelSerializer):
    permissoes = PermissaoSerializer(many=True, read_only=True)
    
    class Meta:
        model = GrupoPermissao
        fields = '__all__'

class UsuarioPermissaoSerializer(serializers.ModelSerializer):
    permissao = PermissaoSerializer(read_only=True)
    
    class Meta:
        model = UsuarioPermissao
        fields = '__all__'

class LogAcessoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.usuario.get_full_name', read_only=True)
    
    class Meta:
        model = LogAcesso
        fields = '__all__' 