import { useEffect, useState } from "react"

interface Call {
	call_id: number
	timestamp: string
	phone_number: string
	summary_text: string
	customer_id?: number
	customer_name?: string
}

interface Customer {
	customer_id: number
	name: string
}

export default function CommLog() {
	const [calls, setCalls] = useState<Call[]>([])
	const [filteredCalls, setFilteredCalls] = useState<Call[]>([])
	const [customers, setCustomers] = useState<Customer[]>([])
	const [selectedCustomerId, setSelectedCustomerId] = useState<string>("all")
	const [selectedCall, setSelectedCall] = useState<Call | null>(null)

	useEffect(() => {
		const fetchData = async () => {
			const res = await fetch("/api/commlog")
			const data = await res.json()
			setCalls(data.calls)
			setFilteredCalls(data.calls)
			setCustomers(data.customers)
		}
		fetchData()
	}, [])

	const handleFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
		const value = e.target.value
		setSelectedCustomerId(value)

		if (value === "all") {
			setFilteredCalls(calls)
		} else if (value === "non") {
			setFilteredCalls(calls.filter((call) => !call.customer_id))
		} else {
			const id = parseInt(value)
			setFilteredCalls(calls.filter((call) => call.customer_id === id))
		}
	}

	return (
		<div className="p-6 max-w-3xl mx-auto">
			<h1 className="text-2xl font-bold mb-4">CommLog</h1>

			<select
				value={selectedCustomerId}
				onChange={handleFilterChange}
				className="mb-4 p-2 border rounded"
			>
				<option value="all">All Calls</option>
				<option value="non">Non-Customer Calls</option>
				{customers.map((c) => (
					<option key={c.customer_id} value={c.customer_id}>
						{c.name}
					</option>
				))}
			</select>

			<ul className="space-y-2">
				{filteredCalls.map((call) => (
					<li
						key={call.call_id}
						className="p-4 border rounded shadow hover:bg-gray-100 cursor-pointer"
						onClick={() => setSelectedCall(call)}
					>
						<div className="text-sm text-gray-500">{new Date(call.timestamp).toLocaleString()}</div>
						<div className="font-semibold">{call.phone_number}</div>
						{call.customer_name && <div className="text-blue-600">{call.customer_name}</div>}
						<div className="mt-1">{call.summary_text}</div>
					</li>
				))}
			</ul>

			{/* Popup */}
			{selectedCall && (
				<div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
					<div className="bg-white p-6 rounded shadow-lg max-w-xl w-full">
						<h2 className="text-xl font-bold mb-2">Call Details</h2>
						<p><strong>Timestamp:</strong> {new Date(selectedCall.timestamp).toLocaleString()}</p>
						<p><strong>Phone:</strong> {selectedCall.phone_number}</p>
						{selectedCall.customer_name && <p><strong>Customer:</strong> {selectedCall.customer_name}</p>}
						<p className="mt-4"><strong>Summary:</strong><br />{selectedCall.summary_text}</p>

						<button
							onClick={() => setSelectedCall(null)}
							className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
						>
							Close
						</button>
					</div>
				</div>
			)}
		</div>
	)
}
