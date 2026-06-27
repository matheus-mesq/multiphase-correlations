Os arquivos do presente repositório possuem a correlação de Beggs e Brill implementada em Python para a previsão de queda de pressão e do hold up de líquido em escoamentos multifásicos. A correlação de Beggs e Brill consiste em uma ferramento versátil, uma vez que permite simular o escoamento multifásico para todos os ângulos de inclinação do tubo. Sendo assim, o código, além de realizar o cálculo da queda de pressão e do hold up de líquido, também determina o regime de escoamento em questão (segregado, intermitente, distribuído ou de transição).

O arquivo multiphase_equations.py guarda as variáveis de entrada, sendo tais variáveis:
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

O usuário do código deve fornecer os valores de tais variáveis de entrada para o cálculo da queda de pressão e do hold up de líquido. Assim, além de conter as variáveis de entrada, o arquivo multiphase_equations.py também contém as equações da correlação de Beggs e Brill. Quanto ao arquivo payne-Pdrop.csv, este contém um caso com diversos valores das variáveis de entrada para cálculo do perfil de queda de pressão em uma tubulação. Em relação ao arquivo payne-Holdups.csv, este contém um caso com diversos valores das variáveis de entrada para cálculo do hold up de líquido em uma tubulação. Deste modo, o arquivo multiphase_equations.py pode utilizar os dados dos arquivos payne-Pdrop.csv e payne-Holdups.csv como variáveis de entrada. Já o arquivo execute_teste02.py realiza o cálculo do perfil de queda de pressão e do hold up de líquido em uma tubulação a partir dos arquivos mencionados anteriormente. Por fim, o arquivo test.py realiza a verificação da influencia das variáveis de entrada na queda de pressão a partir das equacões implementadas no arquivo multiphase_equations.py. Tal verificação é feita por meio de um gráfico com escala de cores.
