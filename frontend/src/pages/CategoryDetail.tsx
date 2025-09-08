import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import {getCategoryById} from "../services/api/category.ts";

export default function CategoryDetail() {
  const { id } = useParams<{ id: string }>()
  const [Category, setCategory] = useState<any | null>(null)

  useEffect(() => {
    const fetchCategory = async () =>{
        const Category = await getCategoryById(id!)

        setCategory(Category)
    }

    fetchCategory();
  }, [id])

  if (!Category) return <p>Loading Category…</p>

  return (
    <>
      <h1>{Category.name}</h1>
    </>
  )
}
