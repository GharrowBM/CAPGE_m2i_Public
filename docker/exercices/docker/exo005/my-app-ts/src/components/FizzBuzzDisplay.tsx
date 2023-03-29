import classes from './FizzBuzzDisplay.module.css'

const FizzBuzzDisplay = (props: {value: number}) => {
  const getValueAsText = () => {
    if (props.value % 15 === 0 && props.value !== 0) {
      return "FizzBuzz"
    } else if (props.value % 5 === 0 && props.value !== 0) {
      return "Buzz"
    } else if (props.value % 3 === 0 && props.value !== 0) {
      return "Fizz"
    } else return props.value
  }

  const getDisplayClasses = () => {
    return `${((props.value % 5 === 0 || props.value % 3 === 0) && props.value !== 0) && classes.fizzBuzz}`
  }

  const getDisplayStyles = () => {
    return {
      fontSize: "4rem",
      color: props.value % 15 === 0 && props.value !== 0 ? "orange"
              : props.value % 5 === 0 && props.value !== 0 ? "purple"
              : props.value % 3 === 0 && props.value !== 0 ? "red"
              : "black"
    }
  }

  return <span className={getDisplayClasses()} style={getDisplayStyles()}>{getValueAsText()}</span>
}

export default FizzBuzzDisplay