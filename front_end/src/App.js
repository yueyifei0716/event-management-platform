import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/Home/Home";
import HostDashBoard from "./pages/HostDashBoard/HostDashBoard";
import HostRegister from "./pages/HostRegister/HostRegister";
import HostReset from "./pages/HostReset/HostReset";
import HostLogin from "./pages/HostLogin/HostLogin";
import HostActivityList from "./pages/HostActivityList/HostActivityList";
import HostFan from "./pages/HostFan/HostFan";
import HostBroadcast from "./pages/HostBroadcast/HostBroadcast";

import UserDashBoard from "./pages/UserDashBoard/UserDashBoard";
import UserLogin from "./pages/UserLogin/UserLogin";
import UserRegister from "./pages/UserRegister/UserRegister";
import UserReset from "./pages/UserReset/UserReset";
import NewActivity from './pages/NewActivity/NewActivity';
import UserDetail from "./pages/UserDetail/UserDetail";
import UserUpdateDetail from "./pages/UserUpdateDetail/UserUpdateDetail";
import UserAddBalance from "./pages/UserAddBalance/UserAddBalance";
import ActivityDetail from "./pages/ActivityDetail/ActivityDetail";
import UserDetailPublic from "./pages/UserDetailPublic/UserDetailPublic";
import UserBookHost from "./pages/UserBookHost/UserBookHost";
import UserActivityList from "./pages/UserAcitivityList/UserActivityList";
import UserEditAccount from "./pages/UserEditAccount/UserEditAccount";

import TimeSet from "./pages/TimeAct/TimeSet";
import TimePush from "./pages/TimeAct/TimePush";
import ActRecommended from "./pages/ActUserLike/ActUserLike";
import HostForget from './pages/HostForget/HostForget';
import UserForget from './pages/UserForget/UserForget';
import ALLinfor from "./pages/AllInfo/AllInfo";
import ProtectedRoute from './utils/ProtectedRoute';


function App() {
    document.title = "UNeedSleepWell";

    return (
        <Router>
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route path="/host_forget" element={<HostForget />} />
                <Route path="/user_forget" element={<UserForget />} />
                <Route path="/host_register" element={<HostRegister />} />
                <Route path="/user_register" element={<UserRegister />} />
                <Route path="/host_login" element={<HostLogin />} />
                <Route path="/user_login" element={<UserLogin />} />
                <Route path="/activity_detail/:act_id" element={<ActivityDetail />} />
                <Route path="/time_set" element={<TimeSet />} />
                <Route path="/time_push" element={<TimePush />} />
                <Route path="/all_infor" element={<ALLinfor />} />

                <Route element={<ProtectedRoute />}>
                    <Route path="/host_dashboard" element={<HostDashBoard />} />
                    <Route path="/host_reset" element={<HostReset />} />
                    <Route path="/host_activity_list" element={<HostActivityList />} />
                    <Route path="/host_broadcast" element={<HostBroadcast />} />
                    <Route path="/host_fan" element={<HostFan />} />
                    <Route path="/user_dashboard" element={<UserDashBoard />} />
                    <Route path="/user_reset" element={<UserReset />} />
                    <Route path="/user_detail" element={<UserDetail />} />
                    <Route path="/user_update_detail" element={<UserUpdateDetail />} />
                    <Route path="/user_addbalance" element={<UserAddBalance />} />
                    <Route path="/user_activity_list" element={<UserActivityList />} />
                    <Route path="/user_book_host" element={<UserBookHost />} />
                    <Route path="/user_detail_public" element={<UserDetailPublic />} />
                    <Route path="/new_activity" element={<NewActivity />} />
                    <Route path="/act_user_like" element={<ActRecommended />} />
                    <Route path="/user_edit_account" element={<UserEditAccount />} />
                </Route>
            </Routes>
        </Router>
    );
}

export default App;
