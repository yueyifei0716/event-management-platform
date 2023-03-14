import React from 'react'

import { Decoration2, Decoration8 } from '@jiaminghi/data-view-react'

import './TopHeader.css'

export default () => {
  return (
    <div id="top-header">
      <Decoration8 className="header-left-decoration" />
      <Decoration2 className="header-center-decoration" />
      <Decoration8 className="header-right-decoration" reverse={true} />
      <div className="center-title"> Overall Information </div>
    </div>
  )
}
