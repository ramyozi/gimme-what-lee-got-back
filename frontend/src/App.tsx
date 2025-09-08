import { useEffect, useState } from 'react'
import {getCategories} from "./services/api/category.ts";
import {getItems} from "./services/api/item.ts";

function App() {
  const [categories, setCategories] = useState([])
  const [items, setItems] = useState([])

  useEffect(() => {
  const fetchData = async () => {
    const cats = await getCategories()
    const its = await getItems()
    setCategories(cats)
    setItems(its)
  }
  fetchData()
}, [])


  return (
    <div>
      <h1>Gimme What Lee Got</h1>
      <h2>Categories</h2>
      <ul>{categories.map((c: any) => <li key={c.id}>{c.name}</li>)}</ul>
      <h2>Items</h2>
      <ul>{items.map((i: any) => <li key={i.id}>{i.title}</li>)}</ul>
    </div>
  )
}

export default App
