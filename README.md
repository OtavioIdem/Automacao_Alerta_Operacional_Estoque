# Alertas operacionais

Lê uma posição de estoque em CSV, identifica itens abaixo do mínimo e prepara
uma mensagem de alerta. O envio por webhook só é realizado com `--apply` e
`dry_run` desativado.

## Planejamento

1. Definir fonte confiável para o saldo e estoque mínimo.
2. Validar a regra com exemplos de estoque normal, no limite e insuficiente.
3. Rodar em simulação para ajustar a mensagem e responsáveis.
4. Integrar um webhook corporativo apenas após homologação.

## Execução

```powershell
pip install -r requirements.txt
Copy-Item config.example.json config.json
python main.py --config config.json
python main.py --config config.json --apply
```
