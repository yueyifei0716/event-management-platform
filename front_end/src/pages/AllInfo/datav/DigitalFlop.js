import React, { useState, useEffect } from 'react'

import { DigitalFlop, Decoration10 } from '@jiaminghi/data-view-react'

import './DigitalFlop.css'


export default (props) => {
  const { data } = props
  const [digitalFlopData, setData] = useState([])

  useEffect(() => {
   
    let newArr = data.map(v => {
      return ({
        title:v.name,
        number:{
          number: [v.value],
          content: '{nt}',
          toFixed: 2,
          textAlign: 'right',
        }
      })
    })
    setData(newArr)
  }, [data])

  return (
    <div id="digital-flop">
      {digitalFlopData.map((item,i) => (
        <div className="digital-flop-item" key={i}>
          <div className="digital-flop-title">{item.title}</div>
          <div className="digital-flop">
            <DigitalFlop config={item.number} style={{ width: '100px', height: '50px' }} />
            <div className="unit">{item.unit}</div>
          </div>
        </div>
      ))}

      <Decoration10 />
    </div>
  )
}
