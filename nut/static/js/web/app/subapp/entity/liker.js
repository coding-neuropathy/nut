define([
        'Backbone',
        'models/Entity',
        'views/Entity/EntityLikerViewSidebar',
        'views/Entity/EntityLikerViewMobile',
        'views/Entity/UserItemView'
    ],
    function(
        Backbone,
        EntityModel,
        EntityLikerViewSidebar,
        EntityLikerViewMobile,
        UserItemView
){

    var EntityLikerController = Class.extend(
        {

        init: function(entity){
            this.entityModel = entity || this.getEntityModel;
            entity.on('sync',this.entitySync.bind(this));
            entity.fetch();
            //this.likerViewMobile  = new EntityLikerViewMobile({model: this.likerCollection});

        },
        entitySync: function(){

            this.likerCollection = this.getLikerCollection();
            this.likerViewSidebar = new EntityLikerViewSidebar({
                model: this.likerCollection,
                el: '.entity-liker-sidebar-wrapper'
            });
            this.likerViewSidebar.render();
            console.log('entity sync');
        },

        getEntityModel: function(){
            return this.entityModel ||  new Error('can not find entity model');
        },

        getLikerCollection:function(){
            return this.entityModel.getLikeUserCollection();
        }

    });

    //_.extend(EntityLikerController.prototype, Backbone.Events);

    return EntityLikerController;
});