import { useEffect, useState } from 'react'
import { getCategories } from '../services/api/category'
import { getItems } from '../services/api/item'

export default function Home() {
  const [categories, setCategories] = useState<any[]>([])
  const [items, setItems] = useState<any[]>([])

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
    <div className="p-4">
      <h1>Gimme What Lee Got</h1>

      <h2>Categories</h2>
      <ul>{categories.map((c) => <li key={c.id}>{c.name}</li>)}</ul>

      <h2>Items</h2>
      <ul>{items.map((i) => <li key={i.id}>{i.title}</li>)}</ul>
    </div>
  )
}
