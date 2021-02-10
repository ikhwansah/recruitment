if (sessionStorage.client == "true") {
	$('<li><a href="dashboard"><i class="fas fa-home"></i>Dashboard</a></li><li><a href="employee"><i class="fas fa-users"></i>Applicants</a></li><li><a href="jobvacancy"><i class="fas fa-copy"></i>Vacancies</a></li>').appendTo($('.list-unstyled.navbar__list')[0]);
} else {
	menu = JSON.parse(sessionStorage.list_access).menu;
	permission = JSON.parse(sessionStorage.list_access).permission;
	$.each(menu, function(i, valuemenu) {  
	  menu_in = [];    
	  iconmenu = [];   
	  iconsub = [];   
	  countsubmenu = 0 ;
	  $.each(valuemenu.sub_menu, function(i, valuesub) { 
		$.each(permission, function(i, value) {           
			if(value.sub_menu == valuesub.id){  
			  if(value.view == true){
				menu_in.push(valuesub.name);
				iconsub.push(valuesub.icon);
				countsubmenu+=1;  
			  }
			}
		});
	  });      
	  iconmenu.push(valuemenu.icon);
	  if(countsubmenu == 1){
		$('<li><a href="'+ menu_in[0] +'"><i class="'+ iconmenu[0]+'"></i>'+ valuemenu.name +'</a></li>').appendTo($('.list-unstyled.navbar__list')[0]);
	  }else if(countsubmenu > 1){
	  	$('<li class="has-sub"><a class="js-arrow" href="#"><i class="fas fa-angle-double-right"></i>'+ valuemenu.name +'</a><ul class="list-unstyled navbar__sub-list js-sub-list">').appendTo($('.list-unstyled.navbar__list')[0]);
	  	Submenu = document.getElementsByClassName('list-unstyled navbar__sub-list js-sub-list')[document.getElementsByClassName('list-unstyled navbar__sub-list js-sub-list').length-1];
	  	$.each(menu_in, function(i, value) {
		   Item = document.createElement('li');
		   fr = menu_in[i].substr(4);
		   Item.innerHTML='<a href="'+ menu_in[i] +'"><i class="'+ iconsub[i]+'"></i>'+ fr +'</a>';
		   Submenu.appendChild(Item);
		});
	  }
	});
}