$('<div class="image"> <img src="../static/images/icon/default.png" /></div><div class="content"><a class="js-acc-btn" href="#">'+ sessionStorage.name +'</a></div><div class="account-dropdown js-dropdown"><div class="info clearfix"><div class="image"><a href="#"><img src="../static/images/icon/default.png" /></a></div><div class="content"><h5 class="name"><a href="#">'+ sessionStorage.name +'</a></h5><span class="email">'+ sessionStorage.email +'</span></div></div><div class="account-dropdown__body"><div class="account-dropdown__item"><a href="setting"><i class="fa fa-info-circle"></i>Account Info</a></div><div class="account-dropdown__item"><a href="password"><i class="fa fa-lock"></i>Change Password</a></div></div><div class="account-dropdown__footer"><a href="javascript:logout()"><i class="zmdi zmdi-power"></i>Logout</a></div></div>').appendTo($('.account-item.clearfix.js-item-menu')[0]);