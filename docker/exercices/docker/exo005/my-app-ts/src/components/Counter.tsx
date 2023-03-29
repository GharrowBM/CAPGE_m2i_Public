import { useState } from 'react'
import classes from './Counter.module.css'
import FizzBuzzDisplay from './FizzBuzzDisplay'

const Counter = () => {
  const [counterValue, setCounterValue] = useState<number>(0)


  return (
    <div className="container">
      <div className="my-3 row">
        <div className="col-6 offset-3 bg-dark text-light p-3 rounded">
          <h3 className="display-3">FizzBuzz</h3>
          <hr />
          <div className={classes["counter-container"]}>
            <FizzBuzzDisplay value={counterValue} />
            <div className="d-flex w-100 justify-content-between align-self-end">
              <button onClick={() => setCounterValue(counterValue - 1)} disabled={counterValue <= 0}>-</button>
              <button onClick={() => setCounterValue(counterValue + 1)}>+</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Counter