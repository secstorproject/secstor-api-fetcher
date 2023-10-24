# API Fetcher Tester 🚀

Este repositório foi criado com o propósito de realizar testes em APIs de compartilhamento de segredos.

## 🛠 Configurações

As principais configurações para os testes podem ser ajustadas nos seguintes arquivos:

- **parameters.py**: Localizado em `src/utils`, é o local ideal para ajustar as configurações gerais dos testes.
- **main.py**: Aqui, você encontrará configurações específicas, como as variáveis `N` e `K`, que são usadas nas engines de compartilhamento de segredos. Também há um array que define o número de chaves em cada rodada do teste de reconstrução.

## ⚠️ Atenção

Lembre-se: o `N` e `K` definidos para o teste devem coincidir com os utilizados na API que está sendo testada. Para facilitar esse alinhamento, modificamos a forma como esses parâmetros são configurados na API. Agora, basta ajustá-los no arquivo `application.properties` localizado em `src/main/resources` no projeto da API.

## 🌟 Contribuição

👤Contribuidor Principal: [Acacio-coding](https://github.com/Acacio-coding).
