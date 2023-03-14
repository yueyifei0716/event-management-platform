import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import instance from '../../utils/axios';
import { FullScreenContainer } from '@jiaminghi/data-view-react';
import { Charts } from '@jiaminghi/data-view-react';
import Button from '@mui/material/Button';
import TopHeader from './datav/TopHeader';
import DigitalFlop from './datav/DigitalFlop';
import ScrollBoard from './datav/ScrollBoard';
import './datav/index.css';

// reference from  http://datav-react.jiaminghi.com/guide/

export default () => {
  const [option, setoption] = useState({})
  const [data1, setData1] = useState([])
  const [data2, setData2] = useState([])
  const [data3, setData3] = useState([])
  useEffect(() => {
    instance.get('/overall/info').then(res => {
      setData1(res.data.model1 || [])
      setData2(res.data.model2 || [])
      setData3(res.data.model3 || [])
      let obj = {
        series: [
          {
            type: 'pie',
            radius: '50%',
            roseSort: false,
            data: res.data.model3 || [],
            insideLabel: {
              show: false,
            },
            outsideLabel: {
              formatter: '{name} {percent}%',
              labelLineEndLength: 20,
              style: {
                fill: '#fff',
              },
              labelLineStyle: {
                stroke: '#fff',
              },
            },
            roseType: true,
          },
        ],
      }
      setoption(obj)
    })
  }, [])

  // get overall info and return the data
  return (
    <div id="data-view">
      <FullScreenContainer>
        <TopHeader />

        <div className="main-content">
          <DigitalFlop data={data1} />

          <div className="block-left-right-content">

            <div className="block-top-bottom-content">
              <div className="block-top-content">

                <div id="rose-chart">
                  <div className="rose-chart-title"> All Income </div>
                  <Charts option={option} />
                </div>

                <ScrollBoard data={data2} />

              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', margin: '70px' }}>
                <Link to="/">
                  {/* <button className="float-right" variant="contained" size='large' color="primary"> Back to home page </button> */}
                  <Button variant="contained" size="medium">
                    Back to home page
                  </Button>
                </Link>
              </div>
            </div>

          </div>

        </div>
      </FullScreenContainer>

    </div>
  )
}