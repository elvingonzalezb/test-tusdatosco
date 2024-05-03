import React, { useContext, useEffect, useState } from "react";
import Error from "./Error";
import { UserContext } from "../auth/Token";

const Causas = () => {
  const [token] = useContext(UserContext);
  const [numDocument, setNumDocument] = useState("");
  const [causas, setCausas] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [loaded, setLoaded] = useState(false);

  const handleChange = (event) => {
    setNumDocument(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (numDocument.trim() !== "") {
      await getCausas(numDocument);
    } else {
      await getAllCausas();
    }
  };

  const getCausas = async (numDocument) => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(`/causas/${numDocument}`, requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong");
    } else {
      const data = await response.json();
      setCausas([data]);
      setLoaded(true);
    }
  };

  const getAllCausas = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/causas", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong");
    } else {
      const data = await response.json();
      setCausas(data);
      setLoaded(true);
    }
  };

  useEffect(() => {
    getAllCausas();
  }, []);

  return (
    <>
        <div class="field is-grouped">
            <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
                <p class="control">
                    <input
                        type="text"
                        value={numDocument}
                        onChange={handleChange}
                        placeholder="Enter Num. Document"
                        />

                    <button class="button is-info">
                            Search
                        </button>
                    </p>                  
            </form>     
      </div>
      <Error message={errorMessage} />
      {loaded && causas ? (
        <div>
          {causas.map((item, index) => (
            <div key={index}>
              <h2>Num. Document: {item.numDocument}</h2>
              <table className="table is-fullwidth">
                <thead>
                  <tr>
                    <th>Entry Date</th>
                    <th>Num. Process</th>
                    <th>Action Infraction</th>
                    <th>Id Movement</th>
                  </tr>
                </thead>
                <tbody>
                  {item.causas.map((causa, index) => (
                    <tr key={index}>
                      <td>{causa.entryDate}</td>
                      <td>{causa.numProcess}</td>
                      <td>{causa.actionInfraction}</td>
                      <td>{causa.idMovement}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      ) : (
        <p>Loading</p>
      )}
    </>
  );
};

export default Causas;
