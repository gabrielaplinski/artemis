import { useState } from "react";

const mockTitulos = [
    { titulo: "Fratura", plataforma: "Netflix" },
    { titulo: "Made in Abyss", plataforma: "Netflix" },
    { titulo: "Hellsing", plataforma: ["Netflix", "Prime Video"] },
    { titulo: "Um contratempo", plataforma: "Prime Video" },
    { titulo: "Kanata no Astra", plataforma: "Crunchyroll" },
    {
      titulo: "Kusuriya no Hitorigoto",
      plataforma: ["Netflix", "Crunchyroll", "Prime Video", "HBO Max"],
    },
    {
      titulo: "Bleach",
      plataforma: ["Disney", "Crunchyroll", "Prime Video"],
    },
    { titulo: "Devilman crybaby", plataforma: ["X"] },
    { titulo: "O menino e a garca", plataforma: ["X"] },
    { titulo: "Gleipnir", plataforma: ["X"] },
    { titulo: "Kaguya sama love is war", plataforma: "X" },
    { titulo: "The ewsive samurai", plataforma: "X" },
    { titulo: "Hitori no shita", plataforma: "X" },
    { titulo: "Pisque duas vezes", plataforma: "X" },
    { titulo: "Tokio show", plataforma: "X" },
    { titulo: "Materia escura", plataforma: "X" },
    { titulo: "Code grass", plataforma: "X" },
    { titulo: "Dororo", plataforma: "X" },
    { titulo: "Lord of mysteries", plataforma: "X" },
    { titulo: "The perfection", plataforma: "X" },
    { titulo: "Kiseijuu", plataforma: "X" },
    { titulo: "The boys", plataforma: "X" },
    { titulo: "Yuki hokusho", plataforma: "X" },
    { titulo: "Code breaker", plataforma: "X" },
    { titulo: "Mob psycho 100", plataforma: "X" },
    { titulo: "One piece", plataforma: "X" },
    { titulo: "Oregairu", plataforma: "X" },
    { titulo: "Bungo stray dogs", plataforma: "X" },
    { titulo: "Quiet set", plataforma: "X" },
    { titulo: "O sacrificio do cervo", plataforma: "X" },
    { titulo: "Attack on titan", plataforma: "X" },
    { titulo: "Darling in t he franxx", plataforma: "X" },
    { titulo: "As boas maneiras", plataforma: "X" },
    { titulo: "A substancia", plataforma: "X" },
    { titulo: "Downtown abbey", plataforma: "X" },
    { titulo: "House of dragon", plataforma: "X" },
    { titulo: "Apare ranman", plataforma: "X" },
    { titulo: "Neon genesis evangelion", plataforma: "X" },
    { titulo: "Wotakoi", plataforma: "X" },
    { titulo: "Cac", plataforma: "X" },
    { titulo: "Animal", plataforma: "X" },
    { titulo: "A criada", plataforma: "X" },
    { titulo: "O dia da castracao", plataforma: "X" },
    { titulo: "Fire force", plataforma: "X" },
    { titulo: "The studio", plataforma: "X" },
    { titulo: "Kaze ga tsuyoku fuiteiru", plataforma: "X" },
    { titulo: "Assassination classroom", plataforma: "X" },
    { titulo: "Aya e a bruxa", plataforma: "X" },
    { titulo: "Anohana", plataforma: "X" },
    { titulo: "Boku dake ga inai machi", plataforma: "X" },
    { titulo: "Pssica", plataforma: "X" },
    { titulo: "Gachiakuta", plataforma: "X" },
    { titulo: "Inuyasha", plataforma: "X" },
    { titulo: "Boku no hero", plataforma: "X" },
    { titulo: "Yakusoku no neverland", plataforma: "X" },
    { titulo: "Violet evergarden", plataforma: "X" },
    { titulo: "Fruits basket", plataforma: "X" },
    { titulo: "Takoris original sin", plataforma: "X" },
    { titulo: "Montando a banda", plataforma: "X" },
    { titulo: "Hunter x hunter", plataforma: "X" },
    { titulo: "91 days", plataforma: "X" },
    { titulo: "Solo leveling", plataforma: "X" },
    { titulo: "Love death and robots", plataforma: "X" },
]

export default function App() {
  const [titulos, setTilulos] = useState(mockTitulos)
  const [sorteado, setSorteado] = useState(null)

  function sortear() {
    const escolhido = titulos[Math.floor(Math.random() * titulos.length)]
    setSorteado(escolhido)
  }

  return (
    <div>
      <h1>RoleTela</h1>
      <button onClick={sortear}>Sortear</button>
      {sorteado && <p>{sorteado.titulo}</p>}
    </div>
  )
};
