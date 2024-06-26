# Projeto_IS_Yoparfum
# Sistema de entrada de produtos no estoque da empresa Yoparfum

Este projeto Django compreende dois aplicativos principais: `estoque` e `usuário`. O aplicativo `estoque` lida com o gerenciamento de produtos, enquanto o aplicativo `usuário` gerencia as autenticações e operações relacionadas aos funcioários usuários do sistema.

## Funcionalidades

### Aplicativo Usuário
- **Autenticação de Usuário:** Suporte para login e logout.
- **Gerenciamento de usuários:** Permite cadastrar, listar e excluir colaboradores.
- **Página de Boas-Vindas:** Uma tela de boas-vindas para usuários autenticados.

### Aplicativo Estoque
- **Cadastro de Produtos:** Funcionalidade para adicionar produtos ao estoque.
- **Listagem de Produtos:** Permite consultar produtos, com suporte para filtros por nome, categoria e preço.
- **Dashboard de Estatísticas:** Mostra estatísticas detalhadas dos produtos, incluindo contagem por nome e categoria, e faixas de preço.
- **API de Produtos:** API para acessar informações dos produtos.

## Tecnologias Utilizadas
- Django como framework principal.
- Django REST framework para criação de APIs.
- Pillow para o gerenciamento de imagens dos produtos.

## Configuração e Instalação
1. Clone o repositório.
2. Configure o banco de dados em `settings.py`.
3. Execute as migrações com `python manage.py migrate`.
4. Inicie o servidor com `python manage.py runserver`.

## Permissões
O sistema utiliza decoradores para gestão de permissões, garantindo que apenas usuários autorizados executem certas operações.

## Mais Informações
Para mais detalhes, consulte a documentação interna de cada aplicativo e os comentários no código-fonte.
