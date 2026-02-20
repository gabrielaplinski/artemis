import { useState, useEffect } from "react";
import { listarTitulos, sortearTitulo, filtrarTitulos, sugerirTitulo, adicionarTitulo } from "./services/api";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCircle } from '@fortawesome/free-solid-svg-icons'

export default function App() {
  const [titulos, setTitulos] = useState([]);
  const [sorteado, setSorteado] = useState(null);
  const [filtrosAtivos, setFiltrosAtivos] = useState([]);
  const [query, setQuery] = useState("");
  const [sugestoes, setSugestoes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selecionado, setSelecionado] = useState(null);

  useEffect(() => {
  buscarLista();
  }, []);

  useEffect(() => {
    if(query.length < 2) return setSugestoes([]);

    const timeout = setTimeout(async () => {
      setLoading(true);
      const data = await sugerirTitulo(query);
      console.log(data);
      setSugestoes(data);
      setLoading(false);
    }, 500);
    return () => clearTimeout(timeout);
  }, [query]);

  async function sortear() {
    const escolhido = await sortearTitulo();
    setSorteado(escolhido);   
  }

  async function adicionar() {
    console.log("selecionado:", selecionado);
    if (!selecionado) return;
    await adicionarTitulo(selecionado);
    await buscarLista();
    setQuery("");
    setSelecionado(null);
    setSugestoes([]);
  }

  async function buscarLista() {
    const lista = await listarTitulos();
    setTitulos(Array.isArray(lista) ? lista : []);
  }

  async function filtrar(plataforma) {
    let novaLista
    
    if (filtrosAtivos.includes(plataforma)) {
      novaLista = filtrosAtivos.filter(p => p !== plataforma);
    } else {
      novaLista = [...filtrosAtivos, plataforma]
    }
    
    setFiltrosAtivos(novaLista);

    if (novaLista.length === 0) {
      await buscarLista();
    } else {
      const lista = await filtrarTitulos(novaLista);
      setTitulos(Array.isArray(lista) ? lista : []);
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

  return (
    <div className="bg-gray-900 min-h-screen text-white pt-40 px-80 flex flex-col">
      <h1 className="font-['Nabla'] text-5xl text-start indent-25 font-bold mb-30 w-full">RoleTela</h1>
      <nav className="mb-30 h-50 w-full flex justify-between gap-10" >
        <div className="bg-gray-800 p-10 rounded-lg basis-1/3 flex flex-col items-center">
          <button
            onClick={sortear}
            className="bg-red-800 font-semibold h-10 px-10 py-1 rounded-lg hover:bg-red-600 hover:cursor-pointer active:bg-red-500 transition-colors"
          >
            Sortear
          </button>
          {sorteado && (
            <p className="bg-gray-700 p-2 mt-6 text-xl text-yellow-500 rounded-lg" >
              {sorteado.title} — {sorteado.plataforma}
            </p>
          )}
        </div>

        <div className="w-150 max-w-200 bg-gray-800 p-5 rounded-lg flex flex-wrap justify-center">
          <div className="flex items-start gap-5" >
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Pesquisar novo título"
              className="border h-8 px-3 rounded-lg bg-gray-700 text-white placeholder-gray-400 ouline-none focus:ring-2"
            />
            <button onClick={adicionar} className="bg-yellow-600 font-semibold h-8 px-10 py-1 rounded-lg hover:cursor-pointer transition-colours">Adicionar</button>
          </div>

          {sugestoes.length > 0 && (
            <ul className="w-full overflow-hidden pt-2 grid grid-cols-3 gap-1" >
              {sugestoes.map((item) => (
                <li 
                  key={item.id_api}
                  onClick={() => {
                    setSelecionado(item);
                    setQuery(item.title);
                    setSugestoes([]);
                  }}
                  className="w-full h-16 cursor-pointer rounded-lg bg-gray-950 hover:bg-gray-900 p-2 flex flex-row gap-2 transition-colors"
                >
                  <img src={item.img} alt={item.title} className="w-10 object-cover rounded shrink-0" />
                  <div className="flex flex-col overflow-hidden" >
                    <strong className="text-sm truncate w-full" title={item.title}
                    >
                      {item.title}
                    </strong>
                    <p className="text-xs text-orange-700" >{item.plataforma.join(", ")}</p>
                  </div>
                </li>
              ))}
            </ul>
          )}
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

      <div className="w-full pt-20 flex justify-around" >
        <ul className="pt-10 grid grid-cols-3 gap-10" >
          {titulos.length > 0 ? (
            titulos.map((titulo, index) => (
            <li key={index} className="p-1 w-60 flex flex-col justify-center items-center" >
              {titulo.title}
              <img src={titulo.img} alt="Capa do título" className="w-50" ></img>
              <p className="text-orange-700 text-sm" >{titulo.plataforma}</p>
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
        <aside>
          <h2 className="p" >Títulos assistidos</h2>
        </aside>
      </div>

      <footer className="w-full text-center text-sm py-6 mt-auto" >
        Feito por <a href="#">Gabriela Plinski</a> & <a href="#">Rafael Lunkes</a>
      </footer>
    </div>
  )
};
