import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
      <div className='flex h-screen items-center justify-center bg-slate-900'>
      <h1 className='text-4x1 font-bold text-sky-400 underline'>Tailwind funcionando</h1>
      </div>
        
  )
}

export default App
