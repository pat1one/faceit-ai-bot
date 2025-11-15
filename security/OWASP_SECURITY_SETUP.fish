#!/usr/bin/env fish

echo "🎭 НАЧИНАЕМ OWASP SECURITY AUDIT..."

# 1. УСТАНОВКА ИНСТРУМЕНТОВ БЕЗОПАСНОСТИ
echo "📦 Устанавливаем security инструменты..."
pip install safety bandit trivy detect-secrets pre-commit
npm install --save-dev eslint-plugin-security

# 2. PYTHON DEPENDENCIES SCAN
echo "🔍 Сканируем Python зависимости..."
safety check --full-report --file requirements.txt > security/audits/python_vulnerabilities.txt
bandit -r src/ -f json > security/audits/python_code_security.json

# 3. NODE.JS DEPENDENCIES SCAN  
echo "🔍 Сканируем Node.js зависимости..."
npm audit --audit-level moderate > security/audits/nodejs_audit.txt

# 4. SECRETS DETECTION SETUP
echo "🔐 Настраиваем detect-secrets..."
detect-secrets scan --init > .secrets.baseline
detect-secrets scan --baseline .secrets.baseline

# 5. PRE-COMMIT HOOKS SETUP
echo "🪝 Настраиваем pre-commit hooks..."
cat > .pre-commit-config.yaml << 'YAML_EOF'
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.4.0
  hooks:
  - id: trailing-whitespace
  - id: end-of-file-fixer
  - id: check-yaml
  - id: check-added-large-files
  - id: check-merge-conflict

- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
  - id: detect-secrets
    args: [--baseline, .secrets.baseline]

- repo: https://github.com/psf/black
  rev: 23.9.1
  hooks:
  - id: black
    language_version: python3

- repo: https://github.com/pycqa/flake8
  rev: 6.0.0
  hooks:
  - id: flake8
YAML_EOF

pre-commit install --hook-type pre-commit

echo "✅ SECURITY SETUP COMPLETE!"
