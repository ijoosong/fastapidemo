import { useState, useEffect } from 'react'
import './App.css'

function useDocumentTitle(title) {
  useEffect(() => {
    document.title = "Saying hello to " + title;
  }, [title]);
}

function Pokemon() {
  let [pokemon, setPokemon] = useState("pikachu");
  let [img, setImg] = useState(null);
  let [weaknesses, setWeaknesses] = useState(null);
  let [resistances, setResistances] = useState(null);

  useDocumentTitle(pokemon);

  useEffect(() => {
    let isCurrent = true;
    fetch(`https://fastapipokemon.azurewebsites.net/pokemon/${pokemon}`)
      .then((res) => res.json())
      .then((res) => {
        if (isCurrent) {
          setImg(res.sprite_url);
          setWeaknesses(res.weaknesses);
          setResistances(res.resistances);
        }
      })
      .catch((e) => {
        console.log(`Error: ${e}`);
        isCurrent = false;
      });

    return () => {
      isCurrent = false;
    };
  }, [pokemon]);

  return (
    <>
      <div className="top">
        <input
          type="text"
          placeholder="Enter a Pokémon"
          onChange={(e) => {
            setPokemon(e.target.value);
          }}
        />
      </div>
      <div className="flex">
        <div className="list">
          {weaknesses && `Weaknesses`}
          <ul>
            {weaknesses && weaknesses.map((w) => (
              <li key={w}>{w}</li>
            ))
          }
          </ul>
        </div>
        <div>
          {img && <img src={img} alt={`Sprite for ${pokemon}`} />}
        </div>
        <div className="list">
          {resistances && `Resistances`}
          <ul>
            {resistances && resistances.map((r) => (
              <li key={r}>{r}</li>
            ))
          }
          </ul>
        </div>
      </div>
    </>
  );
};

function App() {
  return (
    <div className="pokemon">
      <Pokemon />
    </div>
  )
}

export default App
