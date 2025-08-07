
# Crie ambiente virtual
python3 -m venv .venv && source .venv/bin/activate

# Instale dependências
pip install -r scripts/requirements.txt

# Rode o script (exemplo com 2 módulos)
python scripts/import_module.py "terraform-aws-modules/ec2-instance/aws,terraform-aws-modules/ecs/aws"

