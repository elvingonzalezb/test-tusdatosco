import React, { useContext, useEffect, useState } from "react";
import Error from "./Error";
import { UserContext } from "../auth/Token";

const Table = () => {
  const [token] = useContext(UserContext);
  const [process, setProcess] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [loaded, setLoaded] = useState(false);  

  //const response = await fetch(`/proceso/get/${id}`, requestOptions);
  const getProcess = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/proceso/get", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the process");
    } else {
      const data = await response.json();
      setProcess(data);
      setLoaded(true);
    }
  };

  useEffect(() => {
    getProcess();
  }, []);

  return (
    <>        
      <Error message={errorMessage} />
      {loaded && process ? (
        <table className="table is-fullwidth">
          <thead>
            <tr>
              <th>Num. Document</th>
              <th>description</th>
              <th>Status</th>
              <th>Total</th>
              <th>Page Process</th>
            </tr>
          </thead>
          <tbody>
            {process.map((proces) => (
              <tr key={proces.id}>
                <td>{proces.document_number}</td>
                <td>{proces.description}</td>
                <td>{proces.status}</td>
                <td>{proces.total_pages}</td>
                <td>{proces.page_number}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Loading</p>
      )}
    </>
  );
};

export default Table;