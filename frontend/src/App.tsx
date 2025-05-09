import { BrowserRouter, Routes, Route, Link } from "react-router-dom"
import CreateCall from "./pages/CreateCall"
import CommLog from "./pages/CommLog"

function App() {
	return (
		<BrowserRouter>
			<div>
				<nav className="p-4 bg-gray-100 border-b flex gap-4 text-blue-700 font-medium">
					<Link to="/create-call" className="hover:underline">Create Call</Link>
					<Link to="/commlog" className="hover:underline">CommLog</Link>
				</nav>

				<Routes>
					<Route path="/create-call" element={<CreateCall />} />
					<Route path="/commlog" element={<CommLog />} />
				</Routes>
			</div>
		</BrowserRouter>
	)
}

export default App
