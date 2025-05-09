import { BrowserRouter, Routes, Route, NavLink, Navigate } from "react-router-dom"
import CreateCall from "./pages/CreateCall"
import CommLog from "./pages/CommLog"
import About from "./pages/About"
function App() {
	return (
		<BrowserRouter>
			<div>
				<nav className="p-6 bg-gray-100 border-b flex gap-6 text-lg font-medium">
					<NavLink
						to="/create-call"
						className={({ isActive }) =>
							isActive ? "text-blue-700 underline" : "text-gray-700 hover:text-blue-600"
						}
					>
						Create Call
					</NavLink>
					<NavLink
						to="/commlog"
						className={({ isActive }) =>
							isActive ? "text-blue-700 underline" : "text-gray-700 hover:text-blue-600"
						}
					>
						CommLog
					</NavLink>
					<NavLink
						to="/about"
						className={({ isActive }) =>
							isActive ? "text-blue-700 underline" : "text-gray-700 hover:text-blue-600"
						}
					>
						About
					</NavLink>
				</nav>
				<Routes>
					<Route path="/" element={<Navigate to="/create-call" replace />} />
					<Route path="/create-call" element={<CreateCall />} />
					<Route path="/commlog" element={<CommLog />} />
					<Route path="/about" element={<About />} />
				</Routes>
			</div>
		</BrowserRouter>
	)
}

export default App
