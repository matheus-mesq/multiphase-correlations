# Correlação de BEGGS e BRILL (1973) Implementada em Python #

Os arquivos do presente repositório possuem a correlação de BEGGS e BRILL (1973) implementada em Python, sendo o código utilizado para a previsão de queda de pressão e do hold up de líquido em escoamentos multifásicos. A correlação de BEGGS e BRILL (1973) consiste em uma ferramento versátil, uma vez que permite simular o escoamento multifásico para todos os ângulos de inclinação do tubo. Deste modo, o código, além de realizar o cálculo da queda de pressão e do hold up de líquido, também determina o regime de escoamento em questão (segregado, intermitente, distribuído ou de transição).

Dentre os arquivos presentes neste repositório, o arquivo multiphase_equations.py guarda as variáveis de entrada, sendo tais variáveis:

- Vazão volumétrica de gás;
- Vazão volumétrica de líquido;
- Diâmetro do tubo;
- Rugosidade do tubo;
- Densidade do líquido;
- Massa molar do gás;
- Tensão superficial;
- Aceleração da gravidade;
- Ângulo de inclinação do tubo;
- Elevação do tubo;
- Comprimento do tubo;
- Temperatura;
- Pressão de entrada.

O usuário do código deve fornecer os valores de tais variáveis de entrada para o cálculo da queda de pressão e do hold up de líquido. Assim, além de conter as variáveis de entrada, o arquivo multiphase_equations.py também contém as equações da correlação de BEGGS e BRILL (1973). Quanto aos arquivos payne-Pdrop.csv e payne-Holdups.csv, estes contém valores das variáveis de entrada retiradas do artigo de PAYNE et al. (1979) para validação da correlação. Deste modo, as variáveis de entrada do arquivo payne-Pdrop.csv são utilizadas para cálculo de queda de pressão e posterior comparação com dados experimentais retirados do artigo. Já as variáveis de entrada do arquivo payne-Holdups.csv são utilizadas para cálculo do hold up de líquido e posterior comparação com dados experimentais retirados do artigo. Com isto, o arquivo multiphase_equations.py pode utilizar os dados dos arquivos payne-Pdrop.csv e payne-Holdups.csv como variáveis de entrada para a validação. Em relação ao arquivo execute_teste.py, este é o arquivo que realiza o cálculo da queda de pressão e do hold up de líquido em uma tubulação utilizando as equações do arquivo multiphase_equations.py e as variáveis de entrada fornecidas, além de determinar os regimes de escoamento. Desta forma, tomando-se os dados dos arquivos payne-Pdrop.csv e payne-Holdups.csv como variáveis de entrada, o arquivo execute_teste.py produz gráficos comparativos entre valores de queda de pressão calculados e experimentais, bem como entre valores de hold up de líquido calculados e experimentais. Por fim, o arquivo test.py produz um gráfico com escala de cores, cuja finalidade é a verificação da influência das variáveis de entrada na queda de pressão a partir das equacões implementadas no arquivo multiphase_equations.py.

<img src="multiphase-correlations/Erros.png" width="500" alt="Erros">
