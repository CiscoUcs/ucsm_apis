#!/bin/sh

echo "Configuring pre-commit hook..."

# make a symbolic link with the pre-commit hook
if [ ! -f ./git/hooks/check_flake8.py ]; then
  ln hooks/check_flake8.py .git/hooks/check_flake8.py
fi
if [ ! -f ./git/hooks/check_ast.py ]; then
  ln hooks/check_ast.py .git/hooks/check_ast.py
fi
if [ ! -f ./git/hooks/check_merge_conflict.py ]; then
  ln hooks/check_merge_conflict.py .git/hooks/check_merge_conflict.py
fi
if [ ! -f ./git/hooks/util.py ]; then
  ln hooks/util.py .git/hooks/util.py
fi

if [ ! -f ./git/hooks/pre-commit ]; then
  ln hooks/pre-commit.py .git/hooks/pre-commit
  echo "Done"
else
  cat <<EOF
A pre-commit hook exists already.
EOF
fi
