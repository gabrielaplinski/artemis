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
    setTitulos(Array.isArray(lista) ? lista : [])
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
      setTitulos(Array.isArray(lista) ? lista : [])
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
    if (novasPlataformas.includes(plataforma)) {
      setNovasPlataformas(novasPlataformas.filter(p => p !== plataforma))
    } else {
      setNovasPlataformas([...novasPlataformas, plataforma])
    }
  }

  return (
    <div className="bg-gray-900 min-h-screen text-white pt-40 px-80 flex flex-col items-center">
      <h1 className="text-5xl text-center font-bold mb-20 w-full">RoleTela</h1>
      <nav className="mb-30 max-h-50 w-full flex gap-50" >
        <div className="bg-gray-800 p-10 rounded-lg basis-1/3 flex flex-col items-center">
          <button
            onClick={sortear}
            className="bg-red-800 font-semibold h-10 px-10 py-1 rounded-lg hover:bg-red-600 hover:cursor-pointer active:bg-red-500 transition-colors"
          >
            Sortear
          </button>
          {sorteado && (
            <p className="bg-gray-700 p-2 mt-6 text-xl text-#fff rounded-lg" >
              {sorteado.titulo} — {sorteado.plataforma}
            </p>
          )}
        </div>
        <div className="bg-gray-800 p-10 rounded-lg grid grid-cols-2 grid-rows-2 gap-4 justify-items-center items-center">
          <input type="text" value={novoTitulo} id="iNovoTitulo" onChange={(e) => setAdicionado(e.target.value)} placeholder="Novo título" className="border px-3 rounded-lg" 
          />
          <button onClick={adicionar} className="bg-green-600 font-semibold h-10 px-10 py-1 rounded-lg hover:cursor-pointer transition-colours" >Adicionar</button>
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
        {titulos.length > 0 ? (
          titulos.map((titulo, index) => (
          <li key={index} className="p-1" >
            {titulo.id} - {titulo.titulo} — {titulo.plataforma}
          </li>
          ))
        ) : filtrosAtivos.length > 0 ? (
          <li className="text-sm text-red-800 col-span-full" >
            No momento não existe nenhum título não assistido nessa(s) plataforma(s)
          </li>
        ) : (
          <li>
            Adicione títulos para começar!
          </li>
        )}
      </ul>

      <footer className="w-full text-center text-sm py-6 mt-auto" >
        Feito por <a href="#">Gabriela Plinski</a> & <a href="#">Rafael Lunkes</a>
      </footer>
    </div>
  )
};
