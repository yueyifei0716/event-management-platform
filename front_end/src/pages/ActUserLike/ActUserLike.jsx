import React, { useState, useContext, useEffect } from 'react';
import instance from '../../utils/axios';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { extractUserId } from "../../utils/Token";
import AuthContext from "../../context/AuthContext";
import { DataGrid } from '@mui/x-data-grid';
import { Link } from "react-router-dom";
import Sidebar from "../../components/SideBar/UserSideBar";
import Topbar from "../../components/TopBar/UserTopBar";


export default function BasicTabs() {

  // initialize the defaut state
  const [value, setValue] = useState(0);
  const [row1, setRow1] = useState([]);
  const [row2, setRow2] = useState([]);
  const [row3, setRow3] = useState([]);
  const { token } = useContext(AuthContext);
  const user_id = extractUserId(token);

  const params = {
    user_id: parseInt(user_id),
    token: token,
  }

  // define every column in the table
  const columns = [
    { field: 'id', headerName: 'ID', width: 40, headerAlign: 'center' },
    {
      field: 'host_name',
      headerName: 'Host Name',
      headerAlign: 'center',
      width: 160,
      renderCell: (params) => {
        return (
          <>
            <Link to={"/user_book_host/"}
              // Here the user logs in to see the detail of the host and can book
              state={{
                host_id: params.row.hold_host,
                host_name: params.row.host_name
              }}
            >
              {params.row.host_name}
            </Link>
          </>
        )
      }
    },
    { field: 'name', headerName: 'Name', width: 100, headerAlign: 'center' },
    { field: 'description', headerName: 'Description', width: 150, headerAlign: 'center' },
    { field: 'type', headerName: 'Type', width: 100, headerAlign: 'center' },
    { field: 'start_date', headerName: 'Start Date', width: 120, headerAlign: 'center' },
    { field: 'end_date', headerName: 'End Date', width: 120, headerAlign: 'center',align : 'center' },
    { field: 'all_ticket', headerName: 'All Ticket', width: 100, headerAlign: 'center' ,align : 'center'},
    { field: 'possible_seats', headerName: 'Possible Seats', width: 120, headerAlign: 'center',align : 'center' },
    { field: 'ticket_money', headerName: 'Ticket Money', width: 120, headerAlign: 'center',align : 'center' },
    {
      field: "action",
      headerName: "Action",
      headerAlign: 'center',
      width: 100,
      renderCell: (params) => {
        return (
          <>
            <Link to={`/activity_detail/${params.row.act_id}`}>
              <button className="productListEdit">Details</button>
            </Link>
          </>
        );
      },
    },
  ];

  // at the beginning, the page will fetch the data from the backend
  useEffect(() => {
    getList1()
  }, [])

  // get the frist kind of recommendation-- popular activity
  const getList1 = () => {
    instance.get(`/activities/user/getpopular`).then(res => {
      setRow1(res.data.activities_info || [])
    })
  };

  // get the second kind of recommendation-- user base similar activity
  const getList2 = () => {
    instance.get(`/activities/user/recommended`, { params }).then(res => {
      console.log(res)
      setRow2(res.data.activities_info || [])
    })
  };

  // get the third kind of recommendation-- description base similar activity
  const getList3 = () => {
    instance.get(`/activities/user/descriptionrecommend`, { params }).then(res => {
      console.log(res)
      setRow3(res.data.activities_info || [])
    })
  };

  // change when tab change
  const handleChange = (event, newValue) => {
    console.log(newValue);
    if (newValue === 1) {
      getList2()
    }
    if (newValue === 2) {
      getList3()
    }
    setValue(newValue);
  };


  return (
    <div className="home">
      <Topbar />

      <div className="container">
        <Sidebar />
        <div className="others">
          <Box sx={{ width: '100%' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={value} onChange={handleChange} centered>
                <Tab label=" The most popular " {...switchTab(0)} />
                <Tab label=" Guess you like " {...switchTab(1)} />
                <Tab label=" Describe similar " {...switchTab(2)} />
              </Tabs>
            </Box>
            <TabPanel value={value} index={0}>
              <Box sx={{ height: 400, width: '100%' }}>
                <DataGrid
                  rows={row1}
                  columns={columns}
                  pageSize={5}
                  rowsPerPageOptions={[5]}
                  disableColumnFilter
                  disableColumnMenu
                  disableSelectionOnClick
                  experimentalFeatures={{ newEditingApi: true }}
                />
              </Box>
            </TabPanel>
            <TabPanel value={value} index={1}>
              <Box sx={{ height: 400, width: '100%' }}>
                <DataGrid
                  rows={row2}
                  columns={columns}
                  pageSize={5}
                  rowsPerPageOptions={[5]}
                  disableColumnFilter
                  disableColumnMenu
                  disableSelectionOnClick
                  experimentalFeatures={{ newEditingApi: true }}
                />

              </Box>
            </TabPanel>
            <TabPanel value={value} index={2}>
              <Box sx={{ height: 400, width: '100%' }}>
                <DataGrid
                  rows={row3}
                  columns={columns}
                  pageSize={5}
                  rowsPerPageOptions={[5]}
                  disableColumnFilter
                  disableColumnMenu
                  disableSelectionOnClick
                  experimentalFeatures={{ newEditingApi: true }}
                />
              </Box>
            </TabPanel>
          </Box>
        </div>
      </div>
    </div>
  );
}

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function switchTab(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}