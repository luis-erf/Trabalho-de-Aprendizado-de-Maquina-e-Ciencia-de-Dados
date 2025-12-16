# Trabalho de Aprendizado de Máquina e Ciência de Dados

Equipe:
- Guilherme José da Silva
- Luis Eduardo Ribeiro Freitas
- Renan Santana Costa

Este trabalho aborda o problema de previsão de temperatura de curto prazo a partir de dados meteorológicos históricos do Instituto Nacional de Meteorologia (INMET), utilizando registros dos anos de 2010 a 2012. O objetivo é prever a temperatura máxima da próxima observação em uma série temporal. Foram realizadas análises exploratórias e testes estatísticos, incluindo ADF, KPSS, ACF e PACF, para caracterização das propriedades da série.

Diferentes modelos foram avaliados, contemplando abordagens estatísticas, de aprendizado de máquina e de aprendizado profundo, especificamente SARIMAX, Random Forest, Gradient Boosting e LSTM. Os dados foram normalizados com StandardScaler e divididos temporalmente em conjuntos de treino, validação e teste. A avaliação foi conduzida por meio das métricas MAE, RMSE e MAPE.

Os resultados indicam bom desempenho na previsão one-step à frente, com destaque para os modelos LSTM e SARIMAX. Além disso, foi explorada uma abordagem baseada em intervalos de confiança como tentativa de previsão de múltiplos passos à frente, cuja implementação completa foi limitada por aspectos de complexidade e organização da série, apontando direções para trabalhos futuros.

