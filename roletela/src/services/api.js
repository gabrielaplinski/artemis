const BASE_URL = "http://localhost:5000"

export async function listarTitulos(plataforma) {
  const url = plataforma
    ? `${BASE_URL}/filmes?plataforma=${plataforma}`
    : `${BASE_URL}/filmes`
  const resposta = await fetch(url)
  return resposta.json()
}

export async function sortearTitulo(plataforma) {
  const url = plataforma
   ? `${BASE_URL}/sortear?plataforma=${plataforma}`
   : `${BASE_URL}/sortear`
  const resposta = await fetch(url)
  return resposta.json()
}

export async function sugerirTitulo(titulo) {
  const resposta = await fetch(`${BASE_URL}/sugerir?titulo=${titulo}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
  return resposta.json()
}

export async function adicionarTitulo(item) {
  const resposta = await fetch(`${BASE_URL}/sugerir/adicionar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item)
  })
  return resposta.json()
}

export async function filtrarTitulos(plataformas) {
  const params = plataformas.map(p => `plataforma=${p}`).join("&")
  const resposta = await fetch(`${BASE_URL}/filmes?${params}`)
  return resposta.json()
}
