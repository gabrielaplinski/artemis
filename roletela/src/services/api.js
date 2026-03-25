const BASE_URL = "http://localhost:5000"

export async function salvarAssistindo(id_api) {
  await fetch(`${BASE_URL}/assistindo`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_api })
  })
}

export async function buscarAssistindo() {
  const resposta = await fetch(`${BASE_URL}/assistindo`)
  return resposta.json()
}

export async function listarTitulos(plataforma) {
  const url = plataforma
    ? `${BASE_URL}/filmes_sorteaveis?plataforma=${plataforma}`
    : `${BASE_URL}/filmes_sorteaveis`
  const resposta = await fetch(url)
  return resposta.json()
}

export async function sortearTitulo(plataformas) {
  const params = plataformas.map(p => `plataforma=${p}`).join("&")
  const url = plataformas
   ? `${BASE_URL}/sortear?${params}`
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
  const resposta = await fetch(`${BASE_URL}/filmes_sorteaveis?${params}`)
  return resposta.json()
}

export async function excluirTitulo(id_api) {
  const resposta = await fetch(`${BASE_URL}/filmes/excluir?id_api=${id_api}`, {
    method: "DELETE",
    headers: {"Content-Type": "application/json"}
  })
  return resposta.json()
}

export async function alterarStatus(id_api, status) {
  const resposta = await fetch(`${BASE_URL}/alterar_status`, {
    method: "POST", 
    headers: {"Content-Type": "application/json"}, 
    body: JSON.stringify({id_api: id_api, status: status})
  })
  return resposta.json()
}

export async function listarAssistidos() {
  const resposta = await fetch(`${BASE_URL}/filmes_assistidos`)
  return resposta.json()
}
