import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import {getItemById} from '../services/api/item'

export default function ItemDetail() {
  const { id } = useParams<{ id: string }>()
  const [item, setItem] = useState<any | null>(null)

  useEffect(() => {
    const fetchItem = async () =>{
        const item = await getItemById(id!)

        setItem(item)
    }

    fetchItem();
  }, [id])

  if (!item) return <p>Loading item…</p>

  return (
    <>
        <h1>{item.title}</h1>
        <h2>{item.description}</h2>
    </>
  )
}
