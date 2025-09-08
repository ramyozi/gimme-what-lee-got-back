import axios from 'axios';


const API_BASE = import.meta.env.VITE_API_BASE as string

export const getCategories = async () => {
  const response = await axios.get(`${API_BASE}/categories/`)
  return response.data
}
