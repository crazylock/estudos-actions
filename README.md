# Repositório: Criação de repositórios com AWS IAM Role

## \uD83D\uDE80 Objetivo

Criar uma role AWS com OIDC configurado para novos repositórios GitHub, usando Terraform.

## \u2699\uFE0F Estrutura

- `.github/workflows/create-aws-role.yml`: workflow reusable que chama Terraform.
- `terraform/`: código Terraform modular.

## \uD83D\uDD25 Tipos de repositório

- `infra`: anexa policies de infraestrutura.
- `app`: anexa policies para aplicações.

## \uD83D\uDCBB Como chamar o workflow

```yaml
jobs:
  create_aws_role:
    uses: your-org/this-repo/.github/workflows/create-aws-role.yml@main
    with:
      repoid: "nome-do-repo"
      repo_type: "infra"
```


## Exemplos de workflow para ECR

Este repositório também inclui uma estrutura de exemplo de um workflow reutilizável para fazer login no Amazon ECR, realizar o build da imagem Docker com argumentos parametrizáveis e realizar o push para o repositório ECR. Veja em `reusable-ecr-action/`.

Nas pastas `app-java/` e `app-python/` há projetos fictícios demonstrando como consumir esse workflow, cada um passando argumentos de build diferentes.
