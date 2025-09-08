import { lazy, Suspense} from 'react'
import { createBrowserRouter, createRoutesFromElements, Route } from 'react-router-dom'
import RootLayout from "./components/layouts/RootLayout.tsx";
import CategoryDetail from "./pages/CategoryDetail.tsx";


const Home = lazy(() => import('./pages/Home'))
const ItemDetail = lazy(() => import('./pages/ItemDetail'))
const Login = lazy(() => import('./pages/Login'))
const Register = lazy(() => import('./pages/Register'))
const NotFound = lazy(() => import('./pages/NotFound'))

const withSuspense = (el: any) => (
  <Suspense fallback={<div style={{ padding: 16 }}>Loading…</div>}>{el}</Suspense>
)

export const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
      <Route index element={withSuspense(<Home />)} />
      <Route path="login" element={withSuspense(<Login/>)}/>
      <Route path="register" element={withSuspense(<Register/>)}/>
      <Route path="item/:id" element={withSuspense(<ItemDetail />)} />
      <Route path="category/:id" element={withSuspense(<CategoryDetail />)} />
      <Route path="*" element={withSuspense(<NotFound />)} />
    </Route>
  )
)
