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

De posse dos arquivos deste repositório, ao se executar o arquivo execute_teste.py, uma das figuras obtidas é a seguinte:

![dP_versus_Testes](dP%20versus%20Testes.png)

Na figura acima, o eixo das abscissas representa os diversos testes realizados para determinação da queda de pressão, enquanto o eixo das ordenadas representa os respectivos valores de queda de pressão. A curva azul é referente aos valores de queda de pressão calculados, enquanto que a curva laranja é referente aos valores experimentais do arquivo payne-Pdrop.csv. Assim, verifica-se uma predominancia dos maiores valores de queda de pressão nos primeiros testes realizados, e dos menores valores nos últimos. Também é possível verificar que as curvas possuem maior proximidade, até mesmo se sobrepondo, nos testes 5 a 25, 52 a 60 e 68 em diante, indicando menores erros absolutos entre os valores calculados e experimentais de queda de pressão em tais testes. Nos demais testes, as maiores diferenças provavelmente ocorrem devido às aproximações realizadas no cálculo, como considerar o gradiente de pressao como sendo independente do comprimento, e às limitações da própria correlação de BEGGS e BRILL (1973), como o fato de se tratar de um modelo homogêneo, ou seja, há uma aproximação simplificada na qual as fases gás e líquida são tidas como uma única fase, sendo esta fase única um sistema pseudo-monofasico.
