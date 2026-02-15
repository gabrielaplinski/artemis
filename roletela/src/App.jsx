import { useState } from "react";
import { listarTitulos, sortearTitulo } from "./services/api";

export default function App() {
  const [titulos, setTilulos] = useState([])
  const [sorteado, setSorteado] = useState(null)

  async function sortear() {
    const escolhido = await sortearTitulo()
    setSorteado(escolhido)    
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-50">
      <h1 className="text-5xl font-bold mb-8">RoleTela</h1>
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
        <p className="mt-6 text-xl text-yellow-700" >
          {sorteado.plataforma}
        </p>
      )}
    </div>
  )
};
