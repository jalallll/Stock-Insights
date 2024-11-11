"use client";

import { useEffect, useState } from "react";
import axios from "axios";

export default function Home() {
    const [data, setData] = useState([]);
    const [symbol, setSymbol] = useState("AAPL");

    const fetchData = async () => {
        try {
            const response = await axios.get(
                `http://localhost:5001/api/data/monthly/${symbol}`
            );
            setData(response.data);
            console.log("we got data");
            console.log(response.data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    // useEffect(() => {
    //     fetchData();
    // }, [symbol]);

    return (
        <div>
            <h1>Financial Dashboard</h1>
            <input
                type="text"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                placeholder="Enter Stock Symbol"
            />
            <button onClick={fetchData}>Fetch Data</button>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Open</th>
                        <th>High</th>
                        <th>Low</th>
                        <th>Close</th>
                        <th>Volume</th>
                    </tr>
                </thead>
                <tbody>
                    {data.length > 0 ? (
                        data.map((row: any, index) => (
                            <tr key={index}>
                                <td>{row.index}</td>
                                <td>{row.Open}</td>
                                <td>{row.High}</td>
                                <td>{row.Low}</td>
                                <td>{row.Close}</td>
                                <td>{row.Volume}</td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan={6}>No data available</td>{" "}
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
}
