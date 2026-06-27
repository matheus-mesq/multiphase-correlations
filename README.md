# Correlações de Beggs e Brill Implementadas em Python #

Os arquivos do presente repositório possuem a correlação de Beggs e Brill implementada em Python, sendo o código utilizado para a previsão de queda de pressão e do hold up de líquido em escoamentos multifásicos. A correlação de Beggs e Brill consiste em uma ferramento versátil, uma vez que permite simular o escoamento multifásico para todos os ângulos de inclinação do tubo. Deste modo, o código, além de realizar o cálculo da queda de pressão e do hold up de líquido, também determina o regime de escoamento em questão (segregado, intermitente, distribuído ou de transição).

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

O usuário do código deve fornecer os valores de tais variáveis de entrada para o cálculo da queda de pressão e do hold up de líquido. Assim, além de conter as variáveis de entrada, o arquivo multiphase_equations.py também contém as equações da correlação de Beggs e Brill. Quanto ao arquivo payne-Pdrop.csv, este contém um exemplo de caso com diversos valores das variáveis de entrada para cálculo do perfil de queda de pressão em uma tubulação. Já o arquivo payne-Holdups.csv contém um exemplo de caso com diversos valores das variáveis de entrada para cálculo do hold up de líquido em uma tubulação. Deste modo, o arquivo multiphase_equations.py pode utilizar os dados dos arquivos payne-Pdrop.csv e payne-Holdups.csv como variáveis de entrada. Em relação ao arquivo execute_teste02.py, este realiza o cálculo do perfil de queda de pressão e do hold up de líquido em uma tubulação a partir dos arquivos mencionados anteriormente, além de determinar os regimes de escoamento. Por fim, o arquivo test.py produz um gráfico com escala de cores, cuja finalidade é a verificação da influência das variáveis de entrada na queda de pressão a partir das equacões implementadas no arquivo multiphase_equations.py.
