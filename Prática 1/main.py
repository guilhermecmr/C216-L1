alunos = {} # Dicionario com os alunos cadastrados (matricula como chave e dados como valor)

cont_curso = {} # Dicionario para contar o numero de alunos do curso 

def gerar_matricula(curso): # Gera a matricula automaticamente baseada no curso
    if curso not in cont_curso:
        cont_curso[curso] = 1
    else:
        cont_curso[curso] += 1

    return f"{curso}{cont_curso[curso]}"

def cadastrar(): # Cadastra um aluno
    nome = input("\nNome: ")
    email = input("Email: ")
    curso = input("Curso: ")
    matricula = gerar_matricula(curso)

    alunos[matricula] = {"nome": nome, "email": email, "curso": curso}

    print(f"\nAluno cadastrado com sucesso!")
    print(f"Matricula: {matricula}\n")

def listar_alunos(): # Lista todos os alunos cadastrados
    if not alunos:
        print("\nNenhum aluno cadastrado!\n")
        return

    print("\nLista de alunos:\n")

    for matricula, dados in alunos.items():
        print(f"Nome: {dados['nome']}")
        print(f"Matricula: {matricula}")
        print(f"Email: {dados['email']}")
        print(f"Curso: {dados['curso']}\n")

def atualizar_aluno(): # Atualiza os dados de um aluno
    matricula = input("\nDigite a matricula: ")

    if matricula in alunos:
        nome = input("Novo nome: ")
        email = input("Novo email: ")
        curso = input("Novo curso: ")

        alunos[matricula]["nome"] = nome
        alunos[matricula]["email"] = email
        alunos[matricula]["curso"] = curso

        print("\nAluno atualizado com sucesso!\n")
    else:
        print("\nAluno nao encontrado.\n")

def deletar_aluno(): # Deleta um aluno
    matricula = input("\nDigite a matricula: ")

    if matricula in alunos:
        del alunos[matricula]
        print("\nAluno removido com sucesso!\n")
    else:
        print("\nAluno nao encontrado.\n")

def menu(): # Menu principal
    while True:
        print("\n1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Atualizar aluno")
        print("4 - Deletar aluno")
        print("5 - Sair")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            atualizar_aluno()
        elif opcao == "4":
            deletar_aluno()
        elif opcao == "5":
            break
        else:
            print("Opção inválida!")

menu()