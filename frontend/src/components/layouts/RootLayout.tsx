import {NavLink, Outlet} from 'react-router-dom'

export default function RootLayout() {

  return (
    <div>
      <header>
        <NavLink to="/">Home</NavLink>
      </header>

      <main style={{ padding: 16 }}>
        <Outlet />
      </main>
    </div>
  )
}
