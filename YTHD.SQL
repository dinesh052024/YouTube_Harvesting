CREATE TABLE DINESH.CHANNEL_DETAILS(ID MEDIUMINT NOT NULL AUTO_INCREMENT,
									CHNL_ID VARCHAR(255),
                                    CHNL_NAME TEXT,
                                    CHNL_DESC TEXT,
                                    CHNL_TYPE VARCHAR(255),
                                    CHNL_VW_CNT INT,
                                    CHNL_SUB_CNT INT,
                                    CHNL_PLY_ID VARCHAR(255),
                                    PRIMARY KEY (ID),
                                    UNIQUE(CHNL_ID));

CREATE TABLE DINESH.VIDEO_DETAILS(  ID MEDIUMINT NOT NULL AUTO_INCREMENT,
                                    CHN_ID MEDIUMINT,
									VID_ID VARCHAR(255),
                                    VID_NAM TEXT,
                                    VID_DESC TEXT,
                                    TAGS  TEXT,
                                    VID_PUB DATE,
                                    VID_VW_CNT INT,
                                    VID_LIK_CNT INT,
                                    VID_DLIK_CNT INT,
                                    VID_FAV_CNT INT,
                                    VID_CMT_CNT INT,
                                    VID_DUT VARCHAR(255),
                                    VID_THBNAIL TEXT,
                                    VID_CAP_STS VARCHAR(255),                                    
                                    PRIMARY KEY (ID),
                                    FOREIGN KEY (CHN_ID)
                                    REFERENCES DINESH.CHANNEL_DETAILS(ID)
                                    ON DELETE CASCADE) ; 
									
CREATE TABLE DINESH.CMT_DETAILS(  ID MEDIUMINT NOT NULL AUTO_INCREMENT,
                                    CHN_ID MEDIUMINT,
									VID_ID MEDIUMINT,
                                    CMT_ID VARCHAR(255),
                                    CMT_TEXT TEXT,
                                    CMT_AUT  TEXT,
                                    CMT_PUB DATE,                                    
                                    PRIMARY KEY (ID),
                                    FOREIGN KEY (CHN_ID)
                                    REFERENCES DINESH.CHANNEL_DETAILS(ID)
                                    ON DELETE CASCADE) ; 									