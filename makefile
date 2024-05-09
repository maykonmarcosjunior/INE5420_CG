all:
	@echo "make run - rodar o projeto"
	@echo "make clean - remover arquivos temporários e zipar o projeto"
	@echo "make unclean - desfazer o make clean"

run:
	@python3 T1_1/main.py

clean:
	@rm -rf __pycache__ T1_1/__pycache__ T1_1/*.pyc T1_1/*.pyo
	@mv T1_1/teste.py ..
	@zip -r T1.zip T1_1

unclean:
	@mv ../teste.py T1_1
	@rm T1.zip
