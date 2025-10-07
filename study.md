## 🎯 Objetivo do Mutate

No Algoritmo Genético, **mutate** serve para:

1. **Evitar estagnação**
   Se você só usar seleção + crossover, a população tende a convergir rapidamente para soluções parecidas → ótimo local.
   A mutação adiciona **diversidade genética**, permitindo escapar desses pontos de estagnação.

2. **Explorar o espaço de soluções**
   Crossovers recombinam boas rotas, mas só dentro do material genético atual.
   A mutação permite criar **novas combinações** que não existiam antes na população.

3. **Fazer pequenas melhorias locais**
   No caso do TSP/roteamento, uma boa mutação é aquela que troca poucos elementos para testar alternativas próximas.
   Isso ajuda a refinar boas rotas já existentes.

---

## 🔧 Tipos de mutação úteis no TSP

* **Swap mutation**
  Troca dois pontos de posição.

  ```python
  def mutate_swap(route):
      i, j = random.sample(range(len(route)), 2)
      route[i], route[j] = route[j], route[i]
      return route
  ```

* **Insert mutation**
  Remove um ponto e o insere em outra posição.
  Bom para testar mudanças mais estruturais.

* **2-opt mutation**
  Inverte um segmento da rota (equivalente ao algoritmo local 2-opt).
  Esse você já usou → ótimo para eliminar cruzamentos desnecessários.

---

## ⚖️ Como escolher?

* Se quiser **exploração ampla**: use `swap` ou `insert`.
* Se quiser **refinamento local**: use `2-opt`.
* Muita gente mistura: 70% 2-opt, 30% swap, por exemplo.

---

## 🚦 Resumindo

👉 O objetivo da `mutate` **não é destruir a rota**, mas **perturbá-la levemente** para manter diversidade e dar chance de explorar vizinhanças da solução.
Ela deve ser **rara (mutation_rate baixo)** e **pequena (afetando só parte da rota)**.

---

Quer que eu te mostre uma versão híbrida da `mutate`, que combina `swap` e `2-opt` aleatoriamente para equilibrar exploração e refinamento?
