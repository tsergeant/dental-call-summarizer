import { useEffect, useState } from "react"

interface Call {
	call_id: number
	timestamp: string
	phone_number: string
	summary_text: string
	customer_id?: number
	customer_name?: string
	office_person?: string
	transcription_text: string
}

interface Customer {
	customer_id: number
	name: string
}

function formatPhoneNumber(phone: string): string {
	if (phone.length === 10) {
		return `${phone.slice(0, 3)}-${phone.slice(3, 6)}-${phone.slice(6)}`
	}
	return phone
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
			<h2 className="text-xl font-semibold text-gray-800 mb-2">Notes</h2>

			<ul className="list-disc list-inside pl-4">
				<li>
					The drop down filters by customer.
				</li>
				<li>
					There is not pagination. We are working with a small database in this toy app.
				</li>
				<li>
					Click on an entry to call details.
				</li>
			</ul>

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
						<div className="grid gap-4 sm:grid-cols-[auto,1fr]">

							<div className="whitespace-nowrap text-sm text-gray-600">
								<div>{new Date(call.timestamp).toLocaleString()}</div>
								<div>{formatPhoneNumber(call.phone_number)}</div>
								{call.customer_name && <div className="text-blue-700">{call.customer_name}</div>}
							</div>
							<div className="text-gray-800">{call.summary_text}</div>
						</div>
					</li>
				))}
			</ul>

			{/* Popup */}
			{selectedCall && (
				<div className="fixed inset-0 bg-black bg-opacity-50 overflow-y-auto z-50">
					<div className="mt-10 mx-auto bg-white p-6 rounded shadow-lg max-w-2xl w-full">						<h2 className="text-xl font-bold mb-4">Call Details</h2>
						<div className="space-y-2 text-sm text-gray-800">
							<p><strong>Timestamp:</strong> {new Date(selectedCall.timestamp).toLocaleString()}</p>
							<p><strong>Phone:</strong> {formatPhoneNumber(selectedCall.phone_number)}</p>
							{selectedCall.customer_name && (
								<p><strong>Customer:</strong> {selectedCall.customer_name}</p>
							)}
							{selectedCall.office_person && (
								<p><strong>Office Person:</strong> {selectedCall.office_person}</p>
							)}
							<p><strong>Summary:</strong><br />
								<span className="whitespace-pre-wrap block mt-1">{selectedCall.summary_text}</span>
							</p>
							<p><strong>Transcript:</strong><br />
								<span className="whitespace-pre-wrap block mt-1">{selectedCall.transcription_text}</span>
							</p>
						</div>

						<button
							onClick={() => setSelectedCall(null)}
							className="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
						>
							Close
						</button>
					</div>
				</div>
			)}
		</div>
	)
}
