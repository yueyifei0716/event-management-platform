import React from 'react'

import { ScrollBoard } from '@jiaminghi/data-view-react'

import './ScrollBoard.css'
// flowing table
export default (props) => {
  const { data } = props
  
  let newArr = data.map((v,i) => {
    return Object.keys(v)
  })
  let newArr2 = data.map((v,i) => {
    return Object.values(v)
  })
  console.log(newArr);
  console.log(newArr2);
  let config = {
    header: newArr[0],
    data: newArr2,
    align: ['center'],
    headerBGC: '#1981f6',
    headerHeight: 45,
    waitTime:3500,
    hoverPause:false,
    oddRowBGC: 'rgba(0, 44, 81, 0.8)',
    evenRowBGC: 'rgba(10, 29, 50, 0.8)',
  }
  return (
    <div id="scroll-board">
      <ScrollBoard config={config} />
    </div>
  )
}
