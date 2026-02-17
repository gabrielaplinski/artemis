import { useState, useEffect } from "react";
import { adicionarTitulo, listarTitulos, sortearTitulo, filtrarTitulos } from "./services/api";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCircle } from '@fortawesome/free-solid-svg-icons'

export default function App() {
  const [titulos, setTitulos] = useState([])
  const [sorteado, setSorteado] = useState(null)
  const [novoTitulo, setAdicionado] = useState("")
  const [novasPlataformas, setNovasPlataformas] = useState([])
  const [filtrosAtivos, setFiltrosAtivos] = useState([])

  useEffect(() => {
  buscarLista()
  }, [])

  async function sortear() {
    const escolhido = await sortearTitulo()
    setSorteado(escolhido)    
  }

  async function adicionar() {
    await adicionarTitulo(novoTitulo, novasPlataformas)
    await buscarLista()
    setAdicionado("")  
    setNovasPlataformas([])  
  }

  async function buscarLista() {
    const lista = await listarTitulos()
    setTitulos(lista)
  }

  async function filtrar(plataforma) {
    let novaLista
    
    if (filtrosAtivos.includes(plataforma)) {
      novaLista = filtrosAtivos.filter(p => p !== plataforma)
    } else {
      novaLista = [...filtrosAtivos, plataforma]
    }
    
    setFiltrosAtivos(novaLista)

    if (novaLista.length === 0) {
      await buscarLista()
    } else {
      const lista = await filtrarTitulos(novaLista)
      setTitulos(lista)
    }
  }

  function BotaoPlataforma({ nome, onClick, ativo, corIcone}) {
    return (
      <li>
        <button
          onClick={onClick} 
          className={`${ativo ? 'bg-gray-600 hover:bg-gray-500' : 'bg-gray-800 hover:bg-gray-700'} w-32 py-2 rounded-lg hover:cursor-pointer transition-colors`}
        >
          {ativo && (
            <FontAwesomeIcon 
              icon={faCircle}
              className={`${corIcone} scale-50`} 
            />
          )}
          {nome}
        </button>
      </li>
    )
  }

  function qualPlataforma(plataforma) {
    console.log("antes:", novasPlataformas)

    if (novasPlataformas.includes(plataforma)) {
      setNovasPlataformas(novasPlataformas.filter(p => p !== plataforma))
    } else {
      setNovasPlataformas([...novasPlataformas, plataforma])
    }

    console.log("clicou em:", plataforma)
  }   

  function AdicionarPlataforma({ id }) {
    return (
      <label>
            <input 
              type="checkbox"
              checked={novasPlataformas.includes(id)}
              onChange={() => qualPlataforma(id)}  
            />
            {id}
      </label>
    )
  }

  return (
    <div className="bg-gray-900 min-h-screen text-white pt-50 px-80 flex flex-col items-center">
      <h1 className="text-5xl text-center font-bold mb-20 w-full">RoleTela</h1>
      <nav className="mb-10 w-full flex flex-row justify-between" >
        <div className="columns-2" >
          <button
            onClick={sortear}
            className="bg-red-800 hover:bg-red-600 hover:cursor-pointer active:bg-red-500 text-white font-semibold px-6 py-1 rounded-lg transition-colors"
          >
            Sortear
          </button>
          {sorteado && (
            <p className="mt-6 text-xl text-yellow-700" >
              {sorteado.titulo}
            </p>
          )}
          {sorteado && (
            <p className="mt-2 mb-10 text-xl text-yellow-700" >
              {sorteado.plataforma}
            </p>
          )}
        </div>
        <div className="flex items-center justify-center gap-5" >
          <input type="text" value={novoTitulo} id="iNovoTitulo" onChange={(e) => setAdicionado(e.target.value)} placeholder="Novo título" className="border" />
          <AdicionarPlataforma id='Netflix' />
          <AdicionarPlataforma id='Crunchyroll' />
          <AdicionarPlataforma id='Disney' />
          <AdicionarPlataforma id='GloboPlay' />
          <AdicionarPlataforma id='HBOMax' />
          <AdicionarPlataforma id='AppleTV' />
          <AdicionarPlataforma id='PrimeVideo' />
          <button onClick={adicionar} className="bg-green-600 font-semibold px-3 rounded-lg hover:cursor-pointer transition-colours" >Adicionar</button>
        </div>
      </nav>

      <ul className="w-full flex flex-row gap-5 justify-center" >
        <BotaoPlataforma 
          nome="Netflix" 
          onClick={() => filtrar("Netflix")} 
          corIcone="text-purple-500"
          ativo={filtrosAtivos.includes("Netflix")}
        />
        <BotaoPlataforma 
          nome="Crunchyroll" 
          onClick={() => filtrar("Crunchyroll")} 
          corIcone="text-yellow-500"
          ativo={filtrosAtivos.includes("Crunchyroll")}
        />
        <BotaoPlataforma 
          nome="Disney+" 
          onClick={() => filtrar("Disney")} 
          corIcone="text-pink-500"
          ativo={filtrosAtivos.includes("Disney")}
        />
        <BotaoPlataforma 
          nome="GloboPlay" 
          onClick={() => filtrar("GloboPlay")} 
          corIcone="text-red-500"
          ativo={filtrosAtivos.includes("GloboPlay")}
        />
        <BotaoPlataforma 
          nome="HBOMax" 
          onClick={() => filtrar("HBOMax")} 
          corIcone="text-orange-500"
          ativo={filtrosAtivos.includes("HBOMax")}
        />
        <BotaoPlataforma 
          nome="AppleTV" 
          onClick={() => filtrar("AppleTV")} 
          corIcone="text-blue-500"
          ativo={filtrosAtivos.includes("AppleTV")}
        />
        <BotaoPlataforma 
          nome="PrimeVideo" 
          onClick={() => filtrar("Prime Video")} 
          corIcone="text-green-500"
          ativo={filtrosAtivos.includes("Prime Video")}
        />
      </ul>

      <ul className="pt-30 grid grid-cols-3 gap-6" >
        {titulos.map((titulo, index) => (
          <li key={index} className="p-1" >
            {titulo.id} - {titulo.titulo} — {titulo.plataforma}
          </li>
        ))}
      </ul>
      <footer className="w-full text-center text-sm py-6 mt-auto" >
        Feito por <a href="#">Gabriela Plinski</a> & <a href="#">Rafael Lunkes</a>
      </footer>
    </div>
  )
};
