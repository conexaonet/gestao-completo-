from rest_framework import serializers
from .models import GerenciadorSenhas

class GerenciadorSenhasSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=False)
    senha_descriptografada = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    dias_para_expiracao = serializers.SerializerMethodField()
    esta_expirada = serializers.SerializerMethodField()
    
    def validate_arquivo(self, value):
        """Validar arquivo se fornecido"""
        if value:
            try:
                # Verificar tamanho do arquivo (máximo 10MB)
                if value.size > 10 * 1024 * 1024:
                    raise serializers.ValidationError("Arquivo muito grande. Máximo 10MB.")
                
                # Verificar extensão
                allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png']
                file_extension = value.name.lower()
                if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                    raise serializers.ValidationError("Tipo de arquivo não permitido.")
            except Exception as e:
                print(f"Erro na validação de arquivo: {e}")
                raise serializers.ValidationError(f"Erro ao processar arquivo: {str(e)}")
        
        return value
    
    class Meta:
        model = GerenciadorSenhas
        fields = [
            'id', 'titulo', 'url', 'usuario_login', 'senha',
            'senha_descriptografada', 'observacoes', 'arquivo', 'favorito',
            'categoria', 'tags', 'tags_list', 'data_expiracao', 'forca_senha',
            'dias_para_expiracao', 'esta_expirada', 'ultima_alteracao',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em', 'forca_senha', 'ultima_alteracao']
    
    def get_senha_descriptografada(self, obj):
        """Retorna a senha descriptografada apenas para o proprietário"""
        request = self.context.get('request')
        if request and request.user == obj.usuario:
            return obj.get_senha()
        return None
    
    def get_tags_list(self, obj):
        """Retorna lista de tags"""
        return obj.get_tags_list()
    
    def get_dias_para_expiracao(self, obj):
        """Retorna dias para expiração"""
        return obj.dias_para_expiracao()
    
    def get_esta_expirada(self, obj):
        """Retorna se a senha está expirada"""
        return obj.esta_expirada()
    
    def create(self, validated_data):
        try:
            senha = validated_data.pop('senha', None)
            print(f"Dados validados: {validated_data}")
            instance = super().create(validated_data)
            if senha:
                instance.set_senha(senha)
                instance.save()
            print(f"Instância criada: {instance.id}")
            return instance
        except Exception as e:
            print(f"Erro no serializer create: {e}")
            raise e
    
    def update(self, instance, validated_data):
        senha = validated_data.pop('senha', None)
        instance = super().update(instance, validated_data)
        if senha:
            instance.set_senha(senha)
            instance.save()
        return instance

class GerenciadorSenhasListSerializer(serializers.ModelSerializer):
    """Serializer para listagem sem expor senhas"""
    tags_list = serializers.SerializerMethodField()
    dias_para_expiracao = serializers.SerializerMethodField()
    esta_expirada = serializers.SerializerMethodField()
    
    class Meta:
        model = GerenciadorSenhas
        fields = [
            'id', 'titulo', 'url', 'usuario_login',
            'observacoes', 'arquivo', 'favorito', 'categoria', 'tags', 'tags_list',
            'data_expiracao', 'forca_senha', 'dias_para_expiracao', 'esta_expirada',
            'ultima_alteracao', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em', 'forca_senha', 'ultima_alteracao']
    
    def get_tags_list(self, obj):
        """Retorna lista de tags"""
        return obj.get_tags_list()
    
    def get_dias_para_expiracao(self, obj):
        """Retorna dias para expiração"""
        return obj.dias_para_expiracao()
    
    def get_esta_expirada(self, obj):
        """Retorna se a senha está expirada"""
        return obj.esta_expirada()

