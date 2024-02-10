from http.server import HTTPServer, BaseHTTPRequestHandler
from googlesearch import search
import random

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("""
            <!DOCTYPE html>
            <html lang="pt-br">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Gerador de Quiz</title>
                <style>
                    body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
            margin: 0;
            padding: 0;
        }

        #quiz-container {
            max-width: 600px;
            margin: 50px auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }

        #question {
            font-size: 18px;
            margin-bottom: 20px;
        }

        #options {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .option {
            background-color: #3498db;
            color: #fff;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }

        .option:hover {
            background-color: #2980b9;
            transform: scale(1.05);
        }

        #result {
            font-size: 20px;
            margin-top: 20px;
            color: #3498db;
            font-weight: bold;
            transition: color 0.3s ease;
        }

        #result.correct {
            color: #2ecc71;
        }

        #result.incorrect {
            color: #e74c3c;
        }

        .option.correct {
            background-color: #2ecc71;
        }

        .option.incorrect {
            background-color: #e74c3c;
        }

        #next-btn {
            background-color: #3498db;
            color: #fff;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 20px;
            display: none; /* Inicialmente oculto até que o usuário escolha uma opção incorreta ou correta */
            transition: background-color 0.3s ease, transform 0.3s ease;
        }

        #next-btn:hover {
            background-color: #2980b9;
            transform: scale(1.05);
        }

        #progress {
            font-size: 16px;
            margin-top: 10px;
        }

        #progress span {
            font-weight: bold;
            color: #3498db;
        }
                </style>
            </head>
            <body>
                <h1>Gerador de Quiz</h1>

                <div id="input-container">
                    <label for="assuntos">Insira os assuntos do seu quiz (separados por vírgula):</label>
                    <input type="text" id="assuntos">
                    <button onclick="gerarQuiz()">Gerar Quiz</button>
                </div>

                <div id="quiz-container" style="display: none;">
                    <div id="question"></div>
                    <div id="options"></div>
                    <div id="result"></div>
                    <button id="next-btn" onclick="proximaPergunta()">Próxima Pergunta</button>
                    <button id="restart-btn" onclick="reiniciarQuiz()">Reiniciar</button>
                </div>
                <div id="progress">Pergunta <span id="current-question">1</span> de <span id="total-questions"></span></div>
                <h2> G.O - @GinCod 🖥️</h2>

            <script>
                function gerarQuiz() {
                    const assuntos = document.getElementById('assuntos').value.split(',');
                    const perguntas = gerarPerguntas(assuntos);
                    
                    document.getElementById('input-container').style.display = 'none';
                    document.getElementById('quiz-container').style.display = 'block';
                    iniciarQuiz(perguntas);
                }

                function gerarPerguntas(assuntos) {
                    const perguntas = [];
                    let totalPerguntas = 0;
                    // Garantir que haja pelo menos 10 perguntas
                    while (totalPerguntas < 10) {
                        for (let i = 0; i < assuntos.length; i++) {
                            // Aqui vamos fazer a pesquisa na web para o assunto atual
                            const resultados = pesquisarWeb(assuntos[i]);
                            // Adicionamos uma pergunta com base nos resultados da pesquisa
                            perguntas.push({
                                pergunta: resultados[Math.floor(Math.random() * resultados.length)],
                                opcoes: ["Opção 1", "Opção 2", "Opção 3", "Opção 4"],
                                opcaoCorreta: Math.floor(Math.random() * 4) + 1
                            });
                            totalPerguntas++;
                            // Se já tivermos 10 perguntas, podemos parar de adicionar
                            if (totalPerguntas >= 10) {
                                break;
                            }
                        }
                    }
                    return perguntas;
                }

                function pesquisarWeb(assunto) {
                    // Aqui utilizamos a biblioteca googlesearch para fazer a pesquisa na web
                    // Estamos limitando a 5 resultados para simplificar
                    const resultados = [];
                    for (let url of search(assunto, num=5, stop=5, pause=2)) {
                        resultados.push(url);
                    }
                    return resultados;
                }

                let perguntaAtual = 0;
                let pontuacao = 0;
                let totalPerguntas = 0;

                const elementoPergunta = document.getElementById('question');
                const elementoOpcoes = document.getElementById('options');
                const elementoResultado = document.getElementById('result');
                const elementoNextBtn = document.getElementById('next-btn');

                function iniciarQuiz(perguntas) {
                    perguntaAtual = 0;
                    pontuacao = 0;
                    totalPerguntas = perguntas.length;

                    exibirPergunta();
                    atualizarProgresso();
                }

                function exibirPergunta() {
                    const perguntaAtualObj = perguntasPersonalizadas[perguntaAtual];
                    elementoPergunta.textContent = perguntaAtualObj.pergunta;

                    elementoOpcoes.innerHTML = "";
                    perguntaAtualObj.opcoes.forEach((opcao, indice) => {
                        const botao = document.createElement('button');
                        botao.textContent = `${indice + 1}. ${opcao}`;
                        botao.classList.add('option');
                        botao.addEventListener('click', () => verificarResposta(indice + 1));
                        elementoOpcoes.appendChild(botao);
                    });
                }

                function verificarResposta(respostaUsuario) {
                    const perguntaAtualObj = perguntasPersonalizadas[perguntaAtual];
                    const opcoes = document.querySelectorAll('.option');
                    const opcaoSelecionada = document.querySelector('.option.selected');

                    if (opcaoSelecionada) {
                        return;
                    }

                    opcoes.forEach((opcao, indice) => {
                        opcao.classList.remove('selected', 'correct', 'incorrect');

                        if (indice + 1 === respostaUsuario) {
                            opcao.classList.add('selected');

                            if (respostaUsuario === perguntaAtualObj.opcaoCorreta) {
                                opcao.classList.add('correct');
                                elementoResultado.textContent = "Resposta correta!";
                                elementoResultado.classList.add('correct');
                                pontuacao++;
                            } else {
                                opcao.classList.add('incorrect');
                                elementoResultado.textContent = `Resposta incorreta. A resposta correta era: ${perguntaAtualObj.opcoes[perguntaAtualObj.opcaoCorreta - 1]}.`;
                                elementoResultado.classList.add('incorrect');
                            }

                            elementoNextBtn.style.display = 'block';
                        }
                    });
                }

                function proximaPergunta() {
                    elementoNextBtn.style.display = 'none';
                    elementoResultado.textContent = "";
                    elementoResultado.classList.remove('correct', 'incorrect');

                    const opcaoSelecionada = document.querySelector('.option.selected');

                    if (opcaoSelecionada) {
                        const respostaUsuario = parseInt(opcaoSelecionada.textContent[0], 10);
                        const perguntaAtualObj = perguntasPersonalizadas[perguntaAtual];

                        if (respostaUsuario === perguntaAtualObj.opcaoCorreta) {
                            pontuacao++;
                        }
                    }

                    perguntaAtual++;

                    if (perguntaAtual < totalPerguntas) {
                        exibirPergunta();
                        atualizarProgresso();
                    } else {
                        exibirResultado();
                    }
                }

                function atualizarProgresso() {
                    document.getElementById('progress').textContent = `Pergunta ${perguntaAtual + 1} de ${totalPerguntas}`;
                }

                function exibirResultado() {
                    const nota = calcularNota();
                    elementoPergunta.textContent = `Você completou o quiz! Sua pontuação é ${pontuacao} de ${totalPerguntas}. ${nota}`;
                    elementoOpcoes.innerHTML = "";
                    document.getElementById('progress').textContent = "";
                    document.getElementById('next-btn').style.display = 'none';
                    document.getElementById('restart-btn').style.display = 'block';
                }

                function calcularNota() {
                    const percentualAcertos = (pontuacao / totalPerguntas) * 100;

                    if (percentualAcertos >= 90) {
                        return '😎';
                    } else if (percentualAcertos >= 80) {
                        return '😊';
                    } else if (percentualAcertos >= 70) {
                        return '😐';
                    } else if (percentualAcertos >= 60) {
                        return '😕';
                    } else {
                        return '😢';
                    }
                }

                function reiniciarQuiz() {
                    document.getElementById('quiz-container').style.display = 'none';
                    document.getElementById('input-container').style.display = 'block';
                    document.getElementById('assuntos').value = '';
                }
            </script>

            </body>
            </html>
            """.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("404 - Not Found".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor iniciado em http://localhost:{port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
