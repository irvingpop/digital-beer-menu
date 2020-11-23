/**
 * @author Irving Popovetsky
 */

var windowheight = $(window).height() - 200;

jQuery(document).ready(function(){ 
  jQuery("#list").jqGrid({
    url:'/admin/bottlemenu_data',
    datatype: 'json',
    jsonReader : { repeatitems: false }, 
    mtype: 'POST',
    colNames:[ 'Edit', 'Beer #', 'Beer Name', 'Brewery', 'Origin', '%ABV', 'Size', 'Unit of Measurement', 'Style', 'Price $','Active', 'Link URL' ],
    colModel :[ 
	{name:'act', index:'act', width:25, align:'center', sortable:false, search:false, formatter:'actions',
		formatoptions:{
			keys: true,
			editformbutton: true,
			editOptions:{height:500,width:800, closeAfterEdit:true, reloadAfterSubmit:true,
                afterSubmit: function () { $(this).jqGrid('setGridParam', {datatype: 'json'}); return [true]; }
            },
			delOptions:{reloadAfterSubmit:true,
                afterSubmit: function () { $(this).jqGrid('setGridParam', {datatype: 'json'}); return [true]; }
            }
        }
	},
	{name:'beerid', index:'beerid', width:55, search:false, hidden:true}, 
	{name:'name', index:'name', width:80, sortable:true, editable:true, edittype:'text', editoptions: {size:30, maxlength: 30}, editrules: {required:true}, searchoptions: { sopt: ['cn', 'eq', 'ne' ]} }, 
	{name:'brewery', index:'brewery', width:60, sortable:true, editable:true, edittype:'text', editoptions: {size:30, maxlength: 30}, editrules: {required:true}, searchoptions: { sopt: ['cn', 'eq', 'ne' ]} }, 
	{name:'origin', index:'origin', width:25, align:'center', sortable:true, editable:true, edittype:'text', editoptions: {size:20, maxlength: 20}, editrules: {required:true}, searchoptions: { sopt: ['cn', 'eq', 'ne' ]} }, 
	{name:'abv', index:'abv', width:25, align:'center',sortable:true,  editable:true, edittype:'text', editoptions: {size:10, maxlength: 10}, editrules: {required:true, number:true}, search:false }, 
	{name:'size', index:'size', width:25, align:'center',sortable:true,  editable:true, edittype:'text', editoptions: {size:10, maxlength: 10}, editrules: {required:true, number:true}, search:false }, 
	{name:'meas', index:'meas', width:25, align:'center', sortable:true, editable:true, edittype:'select', editoptions: {value: {oz:'oz',L:'L'}}, editrules: {required:true}, search:false },
    {name:'style', index:'style', width:25, align:'center', sortable:true, editable:true, edittype:'text', editoptions: {size:20, maxlength: 20}, editrules: {required:true}, searchoptions: { sopt: ['cn', 'eq', 'ne' ]} },
	{name:'price', index:'price', width:25, align:'center',sortable:true,  editable:true, edittype:'text', editoptions: {size:10, maxlength: 10}, editrules: {required:true, number:true}, search:false },
	{name:'active', index:'active', width:25, align:'center', sortable:true, editable:true, edittype:'checkbox', editoptions: { value:"true:false" }, formatter:'checkbox', stype: 'select', searchoptions: { sopt:['eq','ne'], value:':All;true:Yes;false:No' }}, 
	{name:'url', index:'url', width:100, sortable:false, editable:true, edittype:'text', editoptions: {size:100,maxlength:150}, editrules: {required:false} }
    ],
    pager: '#pager',
    rowNum: 1000,
    rowTotal:2000,
    scroll:1,
    hoverrows:false,
    loadonce:true,
    // automatically adjusting window height
    height: windowheight,
//    rowList:[100,200,300,400,500,600,700],
    sortname: 'brewery, name',
    sortorder: 'asc',
    viewrecords: true,
    autowidth: true,
    ignoreCase:true,
    editurl: "/admin/bottlemenu_edit",
    caption: 'Beer Menu Administration',
    gridComplete: function(){ }
  });
  
    jQuery("#list").jqGrid('navGrid',"#pager",{search:false, edit:false, add:true, del:false,
            beforeRefresh: function () { $(this).jqGrid('setGridParam', {datatype: 'json'}); return [true]; }
        },
		   {}, // default settings for delete
		   {height:500,width:800, closeAfterEdit:true, reloadAfterSubmit:true,
               afterSubmit: function () { $(this).jqGrid('setGridParam', {datatype: 'json'}); return [true]; }
           }, // default settings for add
		   {}, //edit
		   {}, // search options
		   {}
);

    jQuery("#list").jqGrid('filterToolbar', {stringResult: false, searchOnEnter: false, defaultSearch : "cn"});

}); 