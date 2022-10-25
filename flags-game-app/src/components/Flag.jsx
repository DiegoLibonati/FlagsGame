import React from 'react'
import "./Flag.css"

export const Flag = ({image, name}) => {
  return (
    <img src={image} alt={name}></img>
  )
}
